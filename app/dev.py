import sys
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class GameReloader(FileSystemEventHandler):
    def __init__(self):
        self.process = None
        self.start_game()

    def start_game(self):
        if self.process:
            self.process.terminate()
            self.process.wait()
        print("\nStarting game...")
        self.process = subprocess.Popen([sys.executable, "run.py"])

    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            print(f"\nDetected change in {event.src_path}")
            self.start_game()

def main():
    event_handler = GameReloader()
    observer = Observer()
    observer.schedule(event_handler, path='src', recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        if event_handler.process:
            event_handler.process.terminate()
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main() 