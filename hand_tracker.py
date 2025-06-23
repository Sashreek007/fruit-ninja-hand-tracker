import cv2
import mediapipe as mp
from mediapipe.tasks.python.vision import GestureRecognizer, GestureRecognizerOptions
from mediapipe.tasks.python.vision import RunningMode


class HandTracker:
    def __init__(self, gesture_model_path):
        # Hands for landmarks
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils

        # Gesture recognizer
        options = GestureRecognizerOptions(
            base_options=mp.tasks.BaseOptions(model_asset_path=gesture_model_path),
            running_mode=RunningMode.IMAGE,
        )
        self.recognizer = GestureRecognizer.create_from_options(options)

        self.landmarks = None
        self.result = None

    def find_hands(self, frame, draw=False):
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.landmarks = self.hands.process(img_rgb)
        if draw and self.landmarks.multi_hand_landmarks:
            for hand_landmarks in self.landmarks.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                )
        return frame

    def find_gesture(self, frame):
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.result = self.recognizer.recognize(
            mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)
        )

    def get_gesture(self):
        if self.result and self.result.gestures:
            return self.result.gestures[0][0].category_name
        return ""

    def get_handed_fingertips(self):
        """
        Always returns [ Right hand tip, Left hand tip ].
        If a hand is missing, it’s None.
        """
        tips = [None, None]

        if self.landmarks and self.landmarks.multi_hand_landmarks:
            for i, hand_landmarks in enumerate(self.landmarks.multi_hand_landmarks):
                label = self.landmarks.multi_handedness[i].classification[0].label
                lm = hand_landmarks.landmark[8]  # index fingertip
                px = int(lm.x * 1280)  # match your frame size!
                py = int(lm.y * 720)
                if label == "Right":
                    tips[0] = (px, py)
                elif label == "Left":
                    tips[1] = (px, py)

        return tips
