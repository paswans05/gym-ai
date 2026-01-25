import sys

class ConsoleFeedback:
    def display(self, message: str):
        # Clear line (ANSI) and print
        # \033[K clears the line
        sys.stdout.write(f"\r\033[K{message}")
        sys.stdout.flush()
