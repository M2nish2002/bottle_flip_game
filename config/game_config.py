import numpy as np

class GameConfig:
    # Color thresholds in HSV
    BLUE_CAP_LOWER = np.array([100, 150, 150])
    BLUE_CAP_UPPER = np.array([140, 255, 255])
    RED_BODY_LOWER = np.array([0, 150, 150])
    RED_BODY_UPPER = np.array([10, 255, 255])
    
    # Game parameters
    MIN_FLIP_HEIGHT = 100  # pixels
    MIN_ROTATION_ANGLE = 350  # degrees
    MAX_DETECTION_LATENCY = 1.0  # seconds
    EXCLUSION_ZONE_RADIUS = 50  # pixels