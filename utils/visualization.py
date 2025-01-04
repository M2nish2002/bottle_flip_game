import cv2
from typing import Tuple

class GameVisualizer:
    @staticmethod
    def draw_markers(frame, cap_pos: Tuple[int, int], body_pos: Tuple[int, int], 
                    exclusion_radius: int, is_cheating: bool):
        if cap_pos and body_pos:
            bottle_center = ((cap_pos[0] + body_pos[0])//2, 
                           (cap_pos[1] + body_pos[1])//2)
            
            cv2.circle(frame, cap_pos, 5, (255, 0, 0), -1)
            cv2.circle(frame, body_pos, 5, (0, 0, 255), -1)
            cv2.circle(frame, bottle_center, exclusion_radius,
                      (0, 255, 0) if not is_cheating else (0, 0, 255), 2)
    
    @staticmethod
    def draw_scores(frame, scores: list):
        cv2.putText(frame, f"Player 1: {scores[0]} Player 2: {scores[1]}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
