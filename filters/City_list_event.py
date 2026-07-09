from PySide6.QtCore import QObject, QEvent, Qt


class CityListFilter(QObject):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def eventFilter(self, obj, event):

        if event.type() == QEvent.KeyPress:

            if obj == self.parent.window.founded_cities:

                if event.key() in (
                    Qt.Key_Return,
                    Qt.Key_Enter,
                    Qt.Key_Right,
                ):
                    self.parent.choose_city()
                    return True

            elif obj == self.parent.window.added_cities:

                if event.key() == Qt.Key_Left:
                    self.parent.unchoose_city()
                    return True

                if event.key() == Qt.Key_Delete:
                    self.parent.delete_city()
                    return True

        return False