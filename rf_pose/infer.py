import numpy as np
import time
from typing import List, Dict

class WiFiDensePose:
    """
    Mock wrapper for a Deep Learning model that converts processed CSI features
    into human pose keypoints (COCO format).
    """
    def __init__(self, model_path: str = None):
        self.model_loaded = True
        print("[RF-Pose] initialized (Mock Model)")

    def infer(self, csi_features: np.ndarray) -> Dict[str, List[float]]:
        """
        Simulate inference. In a real system, this would pass the features
        through a PyTorch/TensorFlow model.
        
        For this MPV, we will generate keypoints that roughly simulate
        a person doing an exercise, oscillating over time to allow
        detection logic to trigger.
        
        Returns:
            Dict of keypoints (x, y) normalized [0, 1]
            Standard COCO Keypoints: 
            0: Nose, 1: LEye, 2: REye, 3: LEar, 4: REar,
            5: LShoulder, 6: RShoulder, 7: LElbow, 8: RElbow,
            9: LWrist, 10: RWrist, 11: LHip, 12: RHip,
            13: LKnee, 14: RKnee, 15: LAnkle, 16: RAnkle
        """
        
        # Use time to drive a simple animation loop (squat-like motion)
        t = time.time()
        cycle = (np.sin(t * 2) + 1) / 2  # 0 to 1 oscillating
        
        # Default standing pose (mid-screen)
        # x is horizontal, y is vertical (0 top, 1 bottom)
        
        mid_x = 0.5
        
        # Head
        nose = [mid_x, 0.1]
        
        # Shoulders (fixed height mostly)
        l_shoulder = [mid_x - 0.1, 0.2]
        r_shoulder = [mid_x + 0.1, 0.2]
        
        # Hips (move down during squat)
        hip_y = 0.5 + (0.2 * cycle) # Generates squat depth movement
        l_hip = [mid_x - 0.08, hip_y]
        r_hip = [mid_x + 0.08, hip_y]
        
        # Knees (move out/down)
        knee_y = hip_y + 0.2
        l_knee = [mid_x - 0.1, knee_y]
        r_knee = [mid_x + 0.1, knee_y]
        
        # Ankles (fixed on ground)
        l_ankle = [mid_x - 0.1, 0.9]
        r_ankle = [mid_x + 0.1, 0.9]
        
        # Arms (just hanging or slight movement)
        l_elbow = [mid_x - 0.12, 0.35]
        r_elbow = [mid_x + 0.12, 0.35]
        l_wrist = [mid_x - 0.12, 0.5]
        r_wrist = [mid_x + 0.12, 0.5]

        # Dummy eyes/ears
        eyes = [0.0, 0.0] 

        keypoints = {
            "nose": nose,
            "left_shoulder": l_shoulder, "right_shoulder": r_shoulder,
            "left_elbow": l_elbow, "right_elbow": r_elbow,
            "left_wrist": l_wrist, "right_wrist": r_wrist,
            "left_hip": l_hip, "right_hip": r_hip,
            "left_knee": l_knee, "right_knee": r_knee,
            "left_ankle": l_ankle, "right_ankle": r_ankle
        }
        
        return keypoints
