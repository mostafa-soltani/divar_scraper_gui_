from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile


class Load_Ui:
    def __init__(self,path) -> None:
        self.path = path

    def load_ui(self,logsignal):
        loader = QUiLoader()

        file = QFile(self.path)


        file.open(QFile.ReadOnly)

        window = loader.load(file)
        
        file.close()

        logsignal.open_app.emit()


        
        return window