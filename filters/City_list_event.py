from PySide6.QtCore import QObject, QEvent, Qt


class CityListFilter(QObject):

    def __init__(self, parent,city_manager):
        super().__init__()
        self.parent = parent
        self.city_manager = city_manager

    def eventFilter(self, obj, event):

        if event.type() == QEvent.KeyPress:

            if obj == self.parent.window.founded_cities:

                if event.key() in (
                    Qt.Key_Return,
                    Qt.Key_Enter,
                    Qt.Key_Right,
                ):
                    self.city_manager.choose_city()
                    return True

            elif obj == self.parent.window.added_cities:

                if event.key() == Qt.Key_Left:
                    self.city_manager.unchoose_city()
                    return True

                if event.key() == Qt.Key_Delete:
                    self.city_manager.delete()
                    return True

        return False