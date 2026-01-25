from flask import Flask, render_template
from flask_socketio import SocketIO
import eventlet
import threading
import argparse
import subprocess
import re
import requests
from realtime.engine import GymEngine

# Initialize Flask and SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

# Global Engine Instance
engine = None
engine_thread = None

def detect_router_model():
    """Attempts to find the router model by scraping the default gateway's title."""
    try:
        # 1. Find Default Gateway (Windows)
        result = subprocess.check_output("ipconfig", text=True)
        # Look for "Default Gateway . . . . . . . . . : 192.168.x.x"
        match = re.search(r"Default Gateway.*: (\d+\.\d+\.\d+\.\d+)", result)
        
        if not match:
            return "Unknown (Gateway not found)"
            
        gateway_ip = match.group(1)
        
        # 2. Scrape Gateway
        try:
            response = requests.get(f"http://{gateway_ip}", timeout=2)
            if response.status_code == 200:
                # 3. Extract Title
                title_match = re.search(r'<title>(.*?)</title>', response.text, re.IGNORECASE)
                if title_match:
                    return f"{title_match.group(1).strip()} ({gateway_ip})"
                return f"Router at {gateway_ip}"
        except:
            pass # Request failed (timeout/refused)
            
        return "Unknown Device"
    except Exception as e:
        return f"Error: {str(e)}"

@socketio.on('connect')
def handle_connect():
    # Send initial status
    # Default to "Simulation" (Mock=True) if engine isn't ready yet, as that's safe.
    if engine:
        monitor_mode = "Simulation" if engine.capturer.mock else "Live CSI"
        is_mock = engine.capturer.mock
    else:
        monitor_mode = "Simulation"
        is_mock = True
        
    router_info = detect_router_model()
    socketio.emit('status_update', {'mode': monitor_mode, 'hardware_warning': is_mock, 'router_model': router_info})

@app.route('/')
def index():
    return render_template('index.html')

def on_frame_processed(data):
    """Callback from GymEngine to push data to frontend"""
    socketio.emit('pose_data', data)

def run_engine(exercise):
    global engine
    engine = GymEngine(exercise_type=exercise, mock=True, on_frame_processed=on_frame_processed)
    engine.start()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="GymAI Web Server")
    parser.add_argument("--exercise", type=str, default="squat", choices=["squat", "pushup", "deadlift"])
    args = parser.parse_args()

    # Start GymEngine in a background thread
    engine_thread = threading.Thread(target=run_engine, args=(args.exercise,), daemon=True)
    engine_thread.start()

    print(f"Starting GymAI Web Server on http://localhost:5000")
    socketio.run(app, debug=True, use_reloader=False)
