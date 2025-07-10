
# your_app/management/commands/train_face_model.py
import os, pickle, cv2, numpy as np
from django.conf import settings
from django.core.management.base import BaseCommand
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from main.face_recognition_service import extract_embedding # Import-ը սերվիսից
from main.models import CustomUser, UserFaceImage

class Command(BaseCommand):
    help = "Trains a flexible face recognition model (SVM or k-NN) based on user count."

    def process_image_field(self, image_field, user_id, embeddings_list, labels_list):
        if not image_field: return
        try:
            image = cv2.imdecode(np.frombuffer(image_field.read(), np.uint8), cv2.IMREAD_COLOR)
            embedding = extract_embedding(image)
            if embedding is not None:
                embeddings_list.append(embedding); labels_list.append(user_id)
                self.stdout.write(f"  - Processed: {image_field.name} for User ID: {user_id}")
            else: self.stdout.write(self.style.WARNING(f"  - No face detected in {image_field.name}"))
        except Exception as e: self.stdout.write(self.style.ERROR(f"  - Error processing {image_field.name}: {e}"))

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting flexible model training..."))
        embeddings, user_ids = [], []

        # 1. Հավաքում ենք բոլոր նկարները
        all_images_to_process, processed_paths = [], set()
        user_images = UserFaceImage.objects.select_related('user').all()
        for img in user_images:
            all_images_to_process.append((img.image, img.user.id)); processed_paths.add(img.image.name)
        users_with_profile = CustomUser.objects.exclude(profile_picture__isnull=True).exclude(profile_picture__exact='')
        for user in users_with_profile:
            if user.profile_picture.name not in processed_paths:
                all_images_to_process.append((user.profile_picture, user.id))
        
        if not all_images_to_process: self.stdout.write(self.style.WARNING("No images found. Exiting.")); return
        
        for image_field, user_id in all_images_to_process: self.process_image_field(image_field, user_id, embeddings, user_ids)
            
        if not embeddings: self.stdout.write(self.style.ERROR("No valid faces found. Model not trained.")); return
        
        total_unique_users = len(set(user_ids))
        self.stdout.write(self.style.NOTICE(f"\nTotal faces processed: {len(embeddings)}. Total unique users: {total_unique_users}"))
        
        model_dir = os.path.join(settings.BASE_DIR, "face_models"); os.makedirs(model_dir, exist_ok=True)
        model_path = os.path.join(model_dir, "facenet_model.pkl") # Փոխենք ֆայլի անունը

        if total_unique_users >= 2:
            self.stdout.write(self.style.SUCCESS("Training advanced SVM model..."))
            label_encoder = LabelEncoder(); labels = label_encoder.fit_transform(user_ids)
            svm_clf = SVC(kernel='linear', probability=True, class_weight='balanced')
            svm_clf.fit(embeddings, labels)
            model_data = {"type": "svm", "classifier": svm_clf, "label_encoder": label_encoder}
            self.stdout.write(self.style.SUCCESS("Advanced SVM model saved."))
        else:
            self.stdout.write(self.style.WARNING("Only one user found. Training a simple k-NN model..."))
            knn_clf = KNeighborsClassifier(n_neighbors=1)
            knn_clf.fit(embeddings, user_ids)
            model_data = {"type": "knn", "classifier": knn_clf}
            self.stdout.write(self.style.SUCCESS("Simple k-NN model saved."))

        with open(model_path, "wb") as f: pickle.dump(model_data, f)