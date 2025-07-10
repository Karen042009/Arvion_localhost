import os, pickle
from collections import Counter
import cv2, mediapipe as mp, numpy as np
from django.conf import settings

_knn_classifier = None
_model_path = os.path.join(settings.BASE_DIR, "face_models", "face_classifier.pkl")
DISTANCE_THRESHOLD, CONFIDENCE_THRESHOLD = 0.9, 0.60

def _extract_embedding(image):
    mp_face_mesh = mp.solutions.face_mesh
    if image is None: return None
    try:
        with mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, min_detection_confidence=0.5, refine_landmarks=True) as face_mesh:
            results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            if not results.multi_face_landmarks: return None
            return np.array([(lm.x, lm.y, lm.z) for lm in results.multi_face_landmarks[0].landmark]).flatten()
    except Exception: return None

def _load_model():
    global _knn_classifier
    if _knn_classifier is None and os.path.exists(_model_path):
        try:
            with open(_model_path, "rb") as f: _knn_classifier = pickle.load(f)
            print("INFO: Face recognition model loaded successfully into memory.")
        except Exception as e: print(f"ERROR: Could not load face recognition model: {e}")

def recognize_face(image_data):
    _load_model()
    if _knn_classifier is None: return None, "Մոդելը բեռնված չէ կամ գոյություն չունի։"
    try: image = cv2.imdecode(np.frombuffer(image_data.read(), np.uint8), cv2.IMREAD_COLOR)
    except Exception: return None, "Նկարի ֆորմատը սխալ է։"
    embedding = _extract_embedding(image)
    if embedding is None: return None, "Նկարում դեմք չի հայտնաբերվել։"
    distances, indices = _knn_classifier.kneighbors([embedding])
    if distances[0][0] > DISTANCE_THRESHOLD: return None, "Դեմքը չի ճանաչվել (բազայում նմանը չի գտնվել)։"
    closest_user_ids = [_knn_classifier.classes_[i] for i in indices[0]]
    most_common_id, best_match_count = Counter(closest_user_ids).most_common(1)[0]
    confidence = best_match_count / _knn_classifier.n_neighbors
    if confidence >= CONFIDENCE_THRESHOLD:
        return most_common_id, f"Ճանաչումը հաջողվեց (վստահություն՝ {confidence:.0%})։"
    else:
        return None, f"Համընկնումը բավարար չէ (վստահություն՝ {confidence:.0%})։"
    