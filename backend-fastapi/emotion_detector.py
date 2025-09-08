import cv2
import numpy as np
import mediapipe as mp
import base64
from io import BytesIO
from PIL import Image
import tensorflow as tf
import os

class EmotionDetector:
    def __init__(self):
        # Initialize MediaPipe
        self.mp_holistic = mp.solutions.holistic
        self.holistic = self.mp_holistic.Holistic(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Load pre-trained model if exists
        self.model = None
        self.labels = None
        
        if os.path.exists("model.h5") and os.path.exists("labels.npy"):
            self.model = tf.keras.models.load_model("model.h5")
            self.labels = np.load("labels.npy")
    
    def detect(self, base64_image: str) -> str:
        """Detect emotion from base64 encoded image"""
        try:
            # Decode base64 image
            image_data = base64.b64decode(base64_image.split(',')[1])
            image = Image.open(BytesIO(image_data))
            
            # Convert to OpenCV format
            frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Process with MediaPipe
            results = self.holistic.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            
            if self.model and self.labels and results.face_landmarks:
                # Extract features
                features = self._extract_features(results)
                
                # Predict emotion
                features_array = np.array(features).reshape(1, -1)
                prediction = self.model.predict(features_array)
                emotion = self.labels[np.argmax(prediction)]
                
                return emotion
            else:
                # Fallback emotion detection based on facial landmarks
                return self._simple_emotion_detection(results)
                
        except Exception as e:
            print(f"Error in emotion detection: {e}")
            return "neutral"
    
    def _extract_features(self, results):
        """Extract features from MediaPipe results"""
        features = []
        
        # Face landmarks
        if results.face_landmarks:
            for landmark in results.face_landmarks.landmark:
                features.append(landmark.x - results.face_landmarks.landmark[1].x)
                features.append(landmark.y - results.face_landmarks.landmark[1].y)
        
        # Left hand landmarks
        if results.left_hand_landmarks:
            for landmark in results.left_hand_landmarks.landmark:
                features.append(landmark.x - results.left_hand_landmarks.landmark[8].x)
                features.append(landmark.y - results.left_hand_landmarks.landmark[8].y)
        else:
            features.extend([0.0] * 42)
        
        # Right hand landmarks
        if results.right_hand_landmarks:
            for landmark in results.right_hand_landmarks.landmark:
                features.append(landmark.x - results.right_hand_landmarks.landmark[8].x)
                features.append(landmark.y - results.right_hand_landmarks.landmark[8].y)
        else:
            features.extend([0.0] * 42)
        
        return features
    
    def _simple_emotion_detection(self, results):
        """Simple emotion detection based on facial landmarks"""
        if not results.face_landmarks:
            return "neutral"
        
        # Simple heuristic-based emotion detection
        # This is a placeholder - in production, use trained model
        landmarks = results.face_landmarks.landmark
        
        # Calculate mouth corners
        mouth_left = landmarks[61].y
        mouth_right = landmarks[291].y
        mouth_center = landmarks[13].y
        
        # Simple smile detection
        if mouth_left < mouth_center and mouth_right < mouth_center:
            return "happy"
        elif mouth_left > mouth_center and mouth_right > mouth_center:
            return "sad"
        else:
            return "neutral"