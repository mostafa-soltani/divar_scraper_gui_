import sys

from PySide6.QtWidgets import QApplication

from gui.main_window import MainWindow


app = QApplication(sys.argv)

window = MainWindow()
window.window.show()

sys.exit(app.exec())

print("1")

app = QApplication(sys.argv)
print("2")

window = MainWindow()
print("3")

window.window.show()
print("4")

sys.exit(app.exec())