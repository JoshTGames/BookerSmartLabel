import threading

class Timer:
    """Allows us to create timers"""

    instance = None
    def __init__(self, timeout: int, callback: callable):
        self.timeout = timeout
        self.callback = callback

        self.thread = None
        self.stop_event = threading.Event()

        Timer.instance = self

    def start(self):
        if self.thread and self.thread.is_alive():
            self.stop_event.set()
            self.thread.join()
        
        self.stop_event.clear()
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()

    def stop(self):
        if self.thread and self.thread.is_alive():
            self.stop_event.set()
            self.thread.join()

    def run(self):
        if not self.stop_event.wait(self.timeout):
            self.callback()
    
    

