from threading import Event


class CancelToken:

    def __init__(self):
        self._event = Event()

    def cancel(self):
        self._event.set()

    def is_cancelled(self):
        return self._event.is_set()
    
    def reset(self):
        self._event.clear()