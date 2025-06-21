import cv2
import mediapipe as mp
from mediapipe.tasks.python.vision import GestureRecognizer, GestureRecognizerOptions


class HandTracker:
    def __init__(self, model_path="gesture_recognizer.task"):
        # --- Setup classic Hands for stable multi-hand landmarks ---
        self.mp_hands = mp.solutions.hands
        self.HandLandmark = self.mp_hands.HandLandmark  # ✅ proper enum!
        self.hands = self.mp_hands.Hands(
            max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7
        )

        # --- Setup GestureRecognizer for robust symbolic gestures ---
        base_options = mp.tasks.BaseOptions(model_asset_path=model_path)
        options = GestureRecognizerOptions(base_options=base_options)
        self.recognizer = GestureRecognizer.create_from_options(options)

        # --- Internal results ---
        self.landmarks = None
        self.gesture_result = None

    def find_hands(self, frame):
        """Use classic Hands API to detect multi-hand landmarks for slicing"""
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.landmarks = self.hands.process(img_rgb)
        return frame

    def find_gesture(self, frame):
        """Use Tasks API to detect symbolic gestures"""
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)
        self.gesture_result = self.recognizer.recognize(mp_image)

    def get_fingertips(self):
        """Return a list of all index finger tips"""
        tips = []
        if self.landmarks and self.landmarks.multi_hand_landmarks:
            for hand in self.landmarks.multi_hand_landmarks:
                lm = hand.landmark[self.HandLandmark.INDEX_FINGER_TIP]
                tips.append((int(lm.x * 1280), int(lm.y * 720)))
        return tips

    def get_gesture(self):
        """Return the top detected gesture name"""
        if self.gesture_result and self.gesture_result.gestures:
            return self.gesture_result.gestures[0][0].category_name
        return None
