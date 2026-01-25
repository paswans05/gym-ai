from typing import Dict, List
from utils.math_utils import calculate_angle

class PushupDetector:
    def __init__(self):
        self.state = "up"
        self.feedback = ""

    def analyze(self, keypoints: Dict[str, List[float]]) -> str:
        """
        Analyzes push-up form.
        """
        if not keypoints:
            return "No Subject"

        # Using right side for visibility assumption
        shoulder = keypoints['right_shoulder']
        elbow = keypoints['right_elbow']
        wrist = keypoints['right_wrist']
        hip = keypoints['right_hip']
        ankle = keypoints['right_ankle']

        # Elbow Angle (Depth)
        elbow_angle = calculate_angle(shoulder, elbow, wrist)
        
        # Body Alignment (Shoulder-Hip-Ankle) - Plank check
        body_angle = calculate_angle(shoulder, hip, ankle)

        status = "Good"

        # Check Plank
        if body_angle < 160:
            status = "Fix Hips (Sagging)"
        
        # Depth/State
        if elbow_angle > 160:
            self.state = "up"
        elif elbow_angle < 90:
            self.state = "down"
            status = "Good Depth" if status == "Good" else status
        
        if self.state == "down" and elbow_angle > 100:
             # Just started going up
             pass

        self.feedback = f"Pushup: {self.state} | Elbow: {int(elbow_angle)} | {status}"
        return self.feedback
