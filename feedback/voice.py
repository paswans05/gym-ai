import threading

class VoiceFeedback:
    def __init__(self):
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            self.available = True
        except ImportError:
            print("pyttsx3 not installed. Voice feedback disabled.")
            self.available = False
        self.last_msg = ""

    def speak(self, message: str):
        if not self.available:
            return
            
        # Avoid spamming the same message
        if message == self.last_msg:
            return
        
        self.last_msg = message
        
        # Run in thread to not block processing
        threading.Thread(target=self._run_speak, args=(message,), daemon=True).start()

    def _run_speak(self, message):
        try:
            self.engine.say(message)
            self.engine.runAndWait()
        except:
            pass
