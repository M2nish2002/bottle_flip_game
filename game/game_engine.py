import cv2
import numpy as np
from config.game_config import GameConfig
from core.bottle_tracker import BottleTracker
from core.cheating_detector import CheatingDetector
from utils.visualization import GameVisualizer

class BottleFlipGame:
    def __init__(self, camera_id=0):
        self.config = GameConfig()
        self.cap = cv2.VideoCapture(camera_id)
        self.bottle_tracker = BottleTracker()
        self.cheating_detector = CheatingDetector()
        self.visualizer = GameVisualizer()
        self.scores = [0, 0]
        self.current_player = 0
        
    def detect_markers(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Detect blue cap
        cap_mask = cv2.inRange(hsv, self.config.BLUE_CAP_LOWER, 
                             self.config.BLUE_CAP_UPPER)
        cap_contours, _ = cv2.findContours(cap_mask, cv2.RETR_EXTERNAL, 
                                         cv2.CHAIN_APPROX_SIMPLE)
        
        # Detect red body
        body_mask = cv2.inRange(hsv, self.config.RED_BODY_LOWER, 
                              self.config.RED_BODY_UPPER)
        body_contours, _ = cv2.findContours(body_mask, cv2.RETR_EXTERNAL, 
                                          cv2.CHAIN_APPROX_SIMPLE)
        
        cap_pos = None
        body_pos = None
        
        if cap_contours:
            largest_cap = max(cap_contours, key=cv2.contourArea)
            M = cv2.moments(largest_cap)
            if M["m00"] != 0:
                cap_pos = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                
        if body_contours:
            largest_body = max(body_contours, key=cv2.contourArea)
            M = cv2.moments(largest_body)
            if M["m00"] != 0:
                body_pos = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                
        return cap_pos, body_pos
    
    def validate_flip(self) -> bool:
        if len(self.bottle_tracker.history) < 2:
            return False
            
        # Check height requirement
        max_height = min(pos[0][1] for pos in self.bottle_tracker.history)
        height_valid = (self.bottle_tracker.history[0][0][1] - max_height 
                       > self.config.MIN_FLIP_HEIGHT)
        
        # Check rotation
        total_rotation = sum(abs(self.bottle_tracker.calculate_rotation()) 
                           for i in range(1, len(self.bottle_tracker.history)))
        rotation_valid = total_rotation > self.config.MIN_ROTATION_ANGLE
        
        # Check time
        time_valid = (self.bottle_tracker.history[-1][2] - 
                     self.bottle_tracker.history[0][2] 
                     < self.config.MAX_DETECTION_LATENCY)
        
        return height_valid and rotation_valid and time_valid
    
    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
                
            # Process frame
            frame = cv2.resize(frame, (640, 480))
            frame = cv2.GaussianBlur(frame, (5, 5), 0)
            
            # Detect bottle markers
            cap_pos, body_pos = self.detect_markers(frame)
            
            if cap_pos and body_pos:
                # Track bottle
                self.bottle_tracker.track_bottle(cap_pos, body_pos)
                
                # Check for cheating
                bottle_center = ((cap_pos[0] + body_pos[0])//2, 
                               (cap_pos[1] + body_pos[1])//2)
                is_cheating = self.cheating_detector.detect_hands_near_bottle(
                    frame, bottle_center, self.config.EXCLUSION_ZONE_RADIUS)
                
                # Visualize game state
                self.visualizer.draw_markers(frame, cap_pos, body_pos,
                                          self.config.EXCLUSION_ZONE_RADIUS,
                                          is_cheating)
                
                # Validate flip
                if self.validate_flip() and not is_cheating:
                    self.scores[self.current_player] += 1
                    self.current_player = 1 - self.current_player
                    self.bottle_tracker = BottleTracker()
            
            # Display scores
            self.visualizer.draw_scores(frame, self.scores)
            
            cv2.imshow('Bottle Flip Game', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        self.cap.release()
        cv2.destroyAllWindows()