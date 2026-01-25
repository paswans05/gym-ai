from typing import Dict, List, Optional
from utils.math_utils import calculate_angle

class SquatDetector:
    def __init__(self):
        self.state = "standing"  # standing, descending, bottom, ascending
        self.feedback = ""
        self.reps = 0
        self.in_rep = False
    
    def analyze(self, keypoints: Dict[str, List[float]]) -> str:
        """
        Analyzes squat form based on keypoints.
        Returns feedback string.
        """
        if not keypoints:
            return "No Subject"

        # Extract relevant joints
        hip = keypoints['left_hip']  # Using left side for 2D MVP
        knee = keypoints['left_knee']
        ankle = keypoints['left_ankle']
        shoulder = keypoints['left_shoulder']
        
        # 1. Depth Check (Hip-Knee-Ankle angle)
        knee_angle = calculate_angle(hip, knee, ankle)
        
        # 2. Back Angle (Vertical-Hip-Shoulder)
        # Construct a vertical point above hip
        vertical_point = [hip[0], hip[1] - 0.5]
        back_angle = calculate_angle(vertical_point, hip, shoulder)

        # State Machine & Feedback
        status = "Good"
        
        # Depth logic
        if knee_angle > 160:
            if self.state == "ascending" and self.in_rep:
                self.reps += 1
                self.in_rep = False
            self.state = "standing"
        elif knee_angle < 100:
            self.state = "bottom"
            self.in_rep = True # Successfully reached depth
        elif knee_angle < 140 and self.state == "standing":
            self.state = "descending"
        elif knee_angle > 100 and self.state == "bottom":
             self.state = "ascending"
        
        if self.state == "bottom":
            if knee_angle > 90: # Not strict parallel for MVP, but decent depth
                status = "Go Lower!"
            else:
                status = "Good Depth"

        # Form check
        if back_angle > 45: # Tipping forward
            status = "Keep Chest Up"

        self.feedback = f"Squat: {self.state} | Reps: {self.reps} | Angle: {int(knee_angle)} | {status}"
        return self.feedback
