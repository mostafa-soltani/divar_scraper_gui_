from PySide6.QtCore import QObject, QEvent, Qt


class CityListFilter(QObject):

    def __init__(self,parent):
        super().__init__()

        self.parent = parent

    def eventFilter(self,Obj, event) -> bool:
        
        if event.type() == QEvent.keyPress:

            if Obj == self.parent.window.founded_cities:

                if event.key() in (Qt.key_return, Qt.key_Enter, Qt.key_right):
                    self.parent.choose_city()
                    return True
                
                
            elif Obj == self.parent.window.added_cities:
                
                if event.key() == Qt.key_left:
                    self.parent.unchoose_city()
                    return True
            if event.key() == Qt.key_Delete:
                self.parent.delete_city()
                return True
        return False