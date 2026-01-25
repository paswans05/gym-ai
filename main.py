import argparse
from realtime.engine import GymEngine

def main():
    parser = argparse.ArgumentParser(description="GymAI: WiFi-CSI Trainer")
    parser.add_argument("--exercise", type=str, default="squat", choices=["squat", "pushup", "deadlift"], help="Exercise to track")
    parser.add_argument("--mock", action="store_true", default=True, help="Use mock CSI data (Default: True)")
    
    args = parser.parse_args()
    
    engine = GymEngine(exercise_type=args.exercise, mock=args.mock)
    engine.start()

if __name__ == "__main__":
    main()
