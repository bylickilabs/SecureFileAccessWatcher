from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os

class FileEventHandler(FileSystemEventHandler):
    def __init__(self, store):
        self.store = store

    def on_any_event(self, event):
        if event.is_directory:
            return
        action = "Modified" if event.event_type == "modified" else event.event_type.capitalize()
        user = os.getlogin() if hasattr(os, "getlogin") else "N/A"
        self.store.add([
            time.strftime("%Y-%m-%d %H:%M:%S"),
            action,
            event.src_path,
            user
        ])

def start_watching(path, store):
    event_handler = FileEventHandler(store)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
