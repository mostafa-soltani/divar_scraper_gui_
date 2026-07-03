from PySide6.QtCore import QObject, Signal

class WorkerSignals(QObject):

    finished = Signal()

    start = Signal()

    progress = Signal(int)

    error = Signal(str)