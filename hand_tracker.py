# hand_tracker.py

import cv2
import mediapipe as mp


class HandTracker:  # <-- make sure this is here exactly
    def __init__(
        self, max_num_hands=2, detection_confidence=0.7, tracking_confidence=0.7
    ):
        self.max_num_hands = max_num_hands

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=self.max_num_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence,
        )
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, frame, draw=True):
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if draw and self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                )

        return frame

    def get_landmarks(self, frame, landmark_index=8):
        h, w, c = frame.shape
        positions = []
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                lm = hand_landmarks.landmark[landmark_index]
                cx, cy = int(lm.x * w), int(lm.y * h)
                positions.append((cx, cy))
        return positions
