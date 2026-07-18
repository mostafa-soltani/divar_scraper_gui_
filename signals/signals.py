from PySide6.QtCore import QObject, Signal


class WorkerSignals(QObject):

    progress = Signal(int)

    current_topic = Signal(str)

    current_city = Signal(str)

    current_database = Signal(str)

    page = Signal(int)

    ad_found = Signal(int)

    ad_saved = Signal(int)

    duplicate = Signal(int)

    connection = Signal(str)

    finished = Signal()

    cancelled = Signal()

    error = Signal(str)


class LogSignals(WorkerSignals):
    date_time = Signal(str)

    topics = Signal(list)

    cities = Signal(dict)

    databases = Signal(list)

    database_type = Signal(int)

    user = Signal(str)

    ads = Signal(list)

    open_app = Signal()

    past_search = Signal()

    start_search = Signal()
    