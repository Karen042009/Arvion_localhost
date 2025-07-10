# your_app/face_recognition_service.py
import os, pickle
import cv2, numpy as np
from django.conf import settings
from keras_facenet import FaceNet

# --- Գլոբալ օբյեկտներ և կարգավորումներ ---
_model_data, _facenet_embedder = None, None
_model_path = os.path.join(settings.BASE_DIR, "face_models", "facenet_model.pkl") # Ճիշտ ֆայլի անունը
SVM_CONFIDENCE_THRESHOLD = 0.75
KNN_DISTANCE_THRESHOLD = 0.7 # FaceNet-ի embedding-ների համար շեմը կարելի է ավելի խիստ դարձնել

def extract_embedding(image):
    """Հանրային ֆունկցիա՝ FaceNet embedding ստանալու համար։"""
    global _facenet_embedder
    if _facenet_embedder is None:
        try: _facenet_embedder = FaceNet(); print("INFO: FaceNet embedder loaded.")
        except Exception as e: print(f"ERROR: Could not initialize FaceNet embedder: {e}"); return None
    if image is None: return None
    try:
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        detections = _facenet_embedder.extract(image_rgb, threshold=0.95)
        return detections[0]['embedding'] if detections else None
    except Exception: return None

def _load_model():
    """Բեռնում է մարզված մոդելը հիշողության մեջ։"""
    global _model_data
    if _model_data is None and os.path.exists(_model_path):
        try:
            with open(_model_path, "rb") as f: _model_data = pickle.load(f)
            model_type = _model_data.get("type", "unknown").upper()
            print(f"INFO: Custom recognition model (TYPE: {model_type}) loaded.")
        except Exception as e: print(f"ERROR: Could not load custom model: {e}")

def recognize_face(image_data):
    _load_model()
    if _model_data is None: return None, "Ճանաչման մոդելը բեռնված չէ։"
    
    try: image = cv2.imdecode(np.frombuffer(image_data.read(), np.uint8), cv2.IMREAD_COLOR)
    except Exception: return None, "Նկարի ֆորմատը սխալ է։"

    embedding = extract_embedding(image)
    if embedding is None: return None, "Նկարում դեմք չի հայտնաբերվել։"
    
    model_type = _model_data.get("type")

    if model_type == "svm":
        svm_clf, label_encoder = _model_data["classifier"], _model_data["label_encoder"]
        probabilities = svm_clf.predict_proba([embedding])[0]
        best_class_index = np.argmax(probabilities)
        confidence = probabilities[best_class_index]
        if confidence >= SVM_CONFIDENCE_THRESHOLD:
            predicted_label = svm_clf.classes_[best_class_index]
            predicted_user_id = label_encoder.inverse_transform([predicted_label])[0]
            return predicted_user_id, f"Ճանաչումը հաջողվեց (վստահություն՝ {confidence:.0%})։"
        else:
            return None, f"Համընկնումը բավարար չէ (վստահություն՝ {confidence:.0%})։"

    elif model_type == "knn":
        knn_clf = _model_data["classifier"]
        distances, _ = knn_clf.kneighbors([embedding], n_neighbors=1)
        if distances[0][0] <= KNN_DISTANCE_THRESHOLD:
            predicted_user_id = knn_clf.predict([embedding])[0]
            return predicted_user_id, "Ճանաչումը հաջողվեց (պարզ մոդել)։"
        else:
            return None, "Դեմքը չի ճանաչվել (պարզ մոդել)։"
            
    else:
        return None, "Մոդելի տեսակն անհայտ է։"