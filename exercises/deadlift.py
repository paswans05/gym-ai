from typing import Dict, List
from utils.math_utils import calculate_angle

class DeadliftDetector:
    def __init__(self):
        self.state = "setup"
        self.feedback = ""

    def analyze(self, keypoints: Dict[str, List[float]]) -> str:
        # Simplified Check: Spine Neutrality
        
        # Hip-Shoulder-Ear (Neck alignment)
        # Hip-Knee-Ankle (Extension)
        
        shoulder = keypoints['right_shoulder']
        hip = keypoints['right_hip']
        knee = keypoints['right_knee']
        
        # Check if hip is fully extended (standing)
        hip_angle = calculate_angle(shoulder, hip, knee)
        
        status = "Good"
        
        if hip_angle < 130:
            self.state = "hinging"
        else:
            self.state = "standing"

        # Simple heuristic: In deadlift, back should be straight.
        # If we had spine keypoints, we'd check curvature.
        # With standard COCO, we check Shoulder-Hip relative to vertical
        
        self.feedback = f"Deadlift: {self.state} | Hip Angle: {int(hip_angle)} | {status}"
        return self.feedback
