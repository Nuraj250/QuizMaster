import time

class QuizTimer:
    def __init__(self):
        self.start_time = None

    def start(self):
        self.start_time = time.time()

    def stop(self):
        if not self.start_time:
            raise ValueError("Timer was not started.")
        return int(time.time() - self.start_time)