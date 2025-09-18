import cv2
import mediapipe as mp
import time
from app.gesture import is_pinch, is_point, is_open   

class MediaPipeRunner:
    def __init__(self, cam_index=0):
        self.cap = cv2.VideoCapture(cam_index)
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
        self.last_point_time = 0
        self.point_hold_triggered = False

    def process(self):
        ret, frame = self.cap.read()
        if not ret:
            return None

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)

        gesture = None
        hand_x, hand_y = None, None

        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0].landmark

            
            hand_x, hand_y = hand[8].x, hand[8].y

            
            if is_pinch(hand):
                gesture = "pinch"
                self.point_hold_triggered = False

            elif is_point(hand):
                
                if not self.point_hold_triggered:
                    if time.time() - self.last_point_time > 3:
                        gesture = "point_hold"
                        self.point_hold_triggered = True
                    else:
                        gesture = "point"
                else:
                    gesture = "point"
            elif is_open(hand):
                gesture = "open"
                self.point_hold_triggered = False
            else:
                gesture = "unknown"

            
            if gesture == "point":
                if self.last_point_time == 0:
                    self.last_point_time = time.time()
            else:
                self.last_point_time = 0

            
            h, w, _ = frame.shape
            for lm in hand:
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

        meta = {"gesture": gesture, "x": hand_x, "y": hand_y}
        return frame, meta
