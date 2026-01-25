# GymAI: Privacy-First Camera-Free Gym Trainer

GymAI detects exercise form using Wi-Fi CSI (Channel State Information) signals, preserving user privacy by eliminating cameras.

## Features
- **Camera-Free**: Uses WiFi-DensePose logic (simulated for MVP) to reconstruct poses.
- **Privacy-First**: No video data is ever captured.
- **Real-Time Feedback**: Biomechanical analysis of squats, pushups, and deadlifts.
- **Modular**: Clean separation of CSI capture, RF pose (ML), and Exercise logic.

## Installation

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the trainer in mock mode (no special hardware required):

```bash
# Default (Squat)
python main.py

# specific exercises
python main.py --exercise pushup
python main.py --exercise deadlift
```

## Architecture

- `csi/`: Handles Wi-Fi signal capture and preprocessing.
- `rf_pose/`: Converts CSI to Keypoints (Mocked for this MVP).
- `exercises/`: Contains biomechanical rules for form validation.
- `feedback/`: Console and Audio feedback systems.
