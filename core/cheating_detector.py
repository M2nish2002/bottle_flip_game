import cv2
import mediapipe as mp
import math
from typing import Tuple

class CheatingDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7)
    
    def detect_hands_near_bottle(self, frame, bottle_pos: Tuple[int, int], 
                               exclusion_radius: int) -> bool:
        results = self.hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for landmark in hand_landmarks.landmark:
                    x, y = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])
                    distance = math.sqrt((x - bottle_pos[0])**2 + (y - bottle_pos[1])**2)
                    if distance < exclusion_radius:
                        return True
        return False