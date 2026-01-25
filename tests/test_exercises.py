import unittest
import sys
import os

# Add root to path so we can import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from exercises.squat import SquatDetector
from exercises.pushup import PushupDetector
from exercises.deadlift import DeadliftDetector

class TestExercises(unittest.TestCase):

    def test_squat_logic(self):
        detector = SquatDetector()
        
        # Test 1: Standing (Hip-Knee-Ankle ~ 180)
        # Mock keypoints for standing
        # Hip=(0,0), Knee=(0,1), Ankle=(0,2) -> Angle 180
        standing_kp = {
            'left_hip': [0, 0], 'left_knee': [0, 1], 'left_ankle': [0, 2],
            'left_shoulder': [0, -1]
        }
        res = detector.analyze(standing_kp)
        self.assertIn("standing", detector.state)
        
        # Test 2: Deep Squat (Hip-Knee-Ankle < 90)
        # Hip=(0,0), Knee=(1,0), Ankle=(0,0) -> 90 deg corner? No, let's use calculator logic
        # A=[0,0], B=[1,0], C=[0,0] is undefined angle logic potentially if overlapping.
        # Let's use clean coordinates.
        # Hip=(0, 0.5), Knee=(0.5, 0.5), Ankle=(0.5, 1.0) -> Angle at Knee?
        # Vector Knee->Hip = [-0.5, 0]
        # Vector Knee->Ankle = [0, 0.5]
        # Angle is 90 degrees.
        squat_kp = {
            'left_hip': [0, 0.5], 'left_knee': [0.5, 0.5], 'left_ankle': [0.5, 1.0],
            'left_shoulder': [0, 0] # Upright back
        }
        res = detector.analyze(squat_kp)
        # Depends on state transition logic in class, it might need to go <100 to change state
        self.assertIn("bottom", detector.state, f"Should be in bottom state. Msg: {res}")
        self.assertIn("Good Depth", res)

    def test_pushup_logic(self):
        detector = PushupDetector()
        
        # Test Up Phase
        up_kp = {
            'right_shoulder': [0,0], 'right_elbow': [0.5,0], 'right_wrist': [1.0,0], # straight arm
            'right_hip': [0,0], 'right_ankle': [-1,0]
        }
        res = detector.analyze(up_kp)
        self.assertIn("up", detector.state)
        
        # Test Down Phase (Elbow bent 90)
        # Shoulder(0,0), Elbow(0,0.5), Wrist(0,0) -> Folded back?
        # Let's do Standard pushup
        # Wrist at (0,0), Elbow at (0, 0.5), Shoulder at (0.5, 0.5) => 90 deg at elbow
        down_kp = {
            'right_shoulder': [0.5, 0.5], 'right_elbow': [0, 0.5], 'right_wrist': [0, 0],
            'right_hip': [0.5, 0.5], 'right_ankle': [1.0, 0.5] # aligned body
        }
        res = detector.analyze(down_kp)
        self.assertIn("down", detector.state, f"Msg: {res}")

    def test_deadlift_logic(self):
        detector = DeadliftDetector()
        # Standing
        # Shoulder(0,2), Hip(0,1), Knee(0,0) -> 180 Line
        standing_kp = {
            'right_shoulder': [0,2], 'right_hip': [0,1], 'right_knee': [0,0]
        }
        res = detector.analyze(standing_kp)
        self.assertIn("standing", detector.state)
        
        # Hinging (Hip Flexion)
        # Shoulder(1,1), Hip(0,1), Knee(0,0)
        # Hip angle: Shoulder-Hip-Knee
        # Vector Hip->Shoulder = [1,0]
        # Vector Hip->Knee = [0,-1]
        # Angle = 90 deg
        hinge_kp = {
            'right_shoulder': [1,1], 'right_hip': [0,1], 'right_knee': [0,0]
        }
        res = detector.analyze(hinge_kp)
        self.assertIn("hinging", detector.state)

if __name__ == '__main__':
    unittest.main()
