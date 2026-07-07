from PySide6.QtWidgets import QMessageBox
from filters.ok_event import KeyFilter


class Database:
    def __init__(self,widget) -> None:
        self.widget = widget
        self.filter = KeyFilter(self.delete)
        self.widget.database_lists.installEventFilter(self.filter)
        pass

    def save(self):

        database_name = self.widget.database_name.text().strip().lower()

        if not database_name:
            QMessageBox.warning(self.widget,'warning','the state section is empty',QMessageBox.StandardButton.Ok)
            return
        
        return database_name
    
    def delete(self):

        selected = self.widget.database_lists.selectedItems()

        if not selected:
            QMessageBox.warning(self.widget,'warning','nothing is selected.',QMessageBox.StandardButton.Ok)
            return
        
        for item in selected:

            self.widget.database_lists.takeItem(
                self.widget.database_lists.row(item)
            )

    def collect(self) -> list:
        databasess = []

        for item in range(self.widget.database_lists.count()):
            city = self.widget.added_cities.item(item).text().lower().strip()

            databasess.append(city)

        return databasess
    
  