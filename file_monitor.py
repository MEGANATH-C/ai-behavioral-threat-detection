import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self.change_count = 0
        self.start_time = time.time()

    def on_modified(self, event):
        if not event.is_directory:
            self.change_count += 1

    def check_activity(self):
        current_time = time.time()
        elapsed = current_time - self.start_time

        if elapsed >= 5:
            if self.change_count > 50:
                print("RANSOMWARE WARNING: High file modification activity detected!")
            else:
                print("File activity normal")

            self.change_count = 0
            self.start_time = current_time


if __name__ == "__main__":
    path = "."
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    print("File monitoring started...")

    try:
        while True:
            event_handler.check_activity()
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
