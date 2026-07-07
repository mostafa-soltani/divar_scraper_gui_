from PySide6.QtCore import QObject, QEvent, Qt


class KeyFilter(QObject):

    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def eventFilter(self, obj, event):

        if (
            event.type() == QEvent.KeyPress
            and event.key() == Qt.Key_Delete
        ):
            self.callback()
            return True

        return False