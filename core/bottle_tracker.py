import math
import time
from typing import Tuple, List
from dataclasses import dataclass

class BottleTracker:
    def __init__(self):
        self.history = []
        self.start_time = None
        self.is_flipping = False
        self.max_height = 0
        self.total_rotation = 0
        
    def track_bottle(self, cap_pos: Tuple[int, int], body_pos: Tuple[int, int]) -> None:
        if cap_pos and body_pos:
            self.history.append((cap_pos, body_pos, time.time()))
            if len(self.history) > 30:  # Keep last 30 frames
                self.history.pop(0)
    
    def calculate_rotation(self) -> float:
        if len(self.history) < 2:
            return 0
        
        prev_cap, prev_body, _ = self.history[-2]
        curr_cap, curr_body, _ = self.history[-1]
        
        prev_angle = math.atan2(prev_cap[1] - prev_body[1], 
                               prev_cap[0] - prev_body[0])
        curr_angle = math.atan2(curr_cap[1] - curr_body[1], 
                               curr_cap[0] - curr_body[0])
        
        rotation = math.degrees(curr_angle - prev_angle)
        if rotation > 180:
            rotation -= 360
        elif rotation < -180:
            rotation += 360
            
        return rotation