from PySide6.QtCore import QObject, Signal


class WorkerSignals(QObject):

    progress = Signal(int)

    current_topic = Signal(str)

    current_city = Signal(str)

    current_database = Signal(str)

    current_connection = Signal(int)

    page = Signal(int)

    ad_found = Signal(int)

    ad_saved = Signal(int)

    duplicate = Signal(int)

    ads = Signal(list)

    finished = Signal()

    cancelled = Signal()

    error = Signal(str)