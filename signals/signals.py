from PySide6.QtCore import QObject, Signal


class WorkerSignals(QObject):

    progress = Signal(int)

    current_topic = Signal(str)
    current_city = Signal(str)
    current_database = Signal(str)

    finished = Signal()

    cancelled = Signal()

    error = Signal(str)