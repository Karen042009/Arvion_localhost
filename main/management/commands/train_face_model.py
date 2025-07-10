import os, pickle, cv2, mediapipe as mp, numpy as np
from django.conf import settings
from django.core.management.base import BaseCommand
from sklearn.neighbors import KNeighborsClassifier
from main.models import UserFaceImage 

mp_face_mesh = mp.solutions.face_mesh
def extract_embedding(image):
    if image is None: return None
    try:
        with mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, min_detection_confidence=0.5, refine_landmarks=True) as face_mesh:
            results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            if not results.multi_face_landmarks: return None
            return np.array([(lm.x, lm.y, lm.z) for lm in results.multi_face_landmarks[0].landmark]).flatten()
    except Exception: return None

class Command(BaseCommand):
    help = "Trains the face recognition model using all dedicated face images."
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting model training..."))
        all_face_images = UserFaceImage.objects.select_related('user').all()
        if not all_face_images: self.stdout.write(self.style.WARNING("No images found for training.")); return
        embeddings, labels = [], []
        for face_image in all_face_images:
            if not face_image.image: continue
            try:
                image = cv2.imdecode(np.frombuffer(face_image.image.read(), np.uint8), cv2.IMREAD_COLOR)
                embedding = extract_embedding(image)
                if embedding is not None:
                    embeddings.append(embedding); labels.append(face_image.user.id)
                    self.stdout.write(f"Processed: User {face_image.user.id}, Image: {face_image.image.name}")
                else: self.stdout.write(self.style.WARNING(f"No face detected in {face_image.image.name}"))
            except Exception as e: self.stdout.write(self.style.ERROR(f"Error processing {face_image.image.name}: {e}"))
        if not embeddings: self.stdout.write(self.style.ERROR("No valid faces found to train the model.")); return
        total_unique_users = len(set(labels))
        num_neighbors = min(total_unique_users, 5) if total_unique_users > 1 else 1
        self.stdout.write(self.style.NOTICE(f"Training KNN model with n_neighbors={num_neighbors}"))
        knn_clf = KNeighborsClassifier(n_neighbors=num_neighbors, algorithm="ball_tree", weights="distance"); knn_clf.fit(embeddings, labels)
        model_dir = os.path.join(settings.BASE_DIR, "face_models"); os.makedirs(model_dir, exist_ok=True)
        with open(os.path.join(model_dir, "face_classifier.pkl"), "wb") as f: pickle.dump(knn_clf, f)
        with open(os.path.join(model_dir, "face_embeddings.pkl"), "wb") as f: pickle.dump(embeddings, f)
        with open(os.path.join(model_dir, "face_labels.pkl"), "wb") as f: pickle.dump(labels, f)
        self.stdout.write(self.style.SUCCESS(f"\nTraining complete! Processed {len(labels)} faces from {total_unique_users} users."))