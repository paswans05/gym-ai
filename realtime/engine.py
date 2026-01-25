import time
from csi.capture import CSICapturer
from csi.preprocess import extract_features
from rf_pose.infer import WiFiDensePose
from feedback.console import ConsoleFeedback
from feedback.voice import VoiceFeedback

# Exercises
from exercises.squat import SquatDetector
from exercises.pushup import PushupDetector
from exercises.deadlift import DeadliftDetector

class GymEngine:
    def __init__(self, exercise_type="squat", mock=True, on_frame_processed=None):
        self.capturer = CSICapturer(mock=mock)
        self.pose_model = WiFiDensePose()
        
        self.console = ConsoleFeedback()
        self.voice = VoiceFeedback()
        self.on_frame_processed = on_frame_processed
        
        if exercise_type == "squat":
            self.detector = SquatDetector()
        elif exercise_type == "pushup":
            self.detector = PushupDetector()
        elif exercise_type == "deadlift":
            self.detector = DeadliftDetector()
        else:
            raise ValueError(f"Unknown exercise: {exercise_type}")
            
        self.running = False

    def start(self):
        self.running = True
        print(f"Starting GymAI Engine... Exercise: {self.detector.__class__.__name__}")
        
        while self.running:
            try:
                # 1. Capture
                frame = self.capturer.get_frame()
                
                # 2. Preprocess
                features = extract_features(frame)
                
                # 3. Inference
                keypoints = self.pose_model.infer(features)
                
                # 4. Analyze
                feedback_text = self.detector.analyze(keypoints)
                
                # 5. Feedback
                self.console.display(feedback_text)
                
                # Optional: Voice trigger on specific faults
                if "Go Lower" in feedback_text: # Example trigger
                     pass 
                     # self.voice.speak("Lower") 

                # Callback for UI
                if self.on_frame_processed:
                    # Get reps if available
                    reps = getattr(self.detector, 'reps', 0)
                    
                    self.on_frame_processed({
                        "keypoints": keypoints,
                        "feedback": feedback_text,
                        "exercise": self.detector.__class__.__name__,
                        "reps": reps
                    }) 

                time.sleep(0.05) # ~20 FPS simulation
                
            except KeyboardInterrupt:
                print("\nStopping...")
                self.running = False

