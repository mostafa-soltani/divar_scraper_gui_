from PySide6.QtWidgets import QMessageBox
from filters.ok_event import KeyFilter


class Database:
    def __init__(self,widget) -> None:
        self.widget = widget
        self.filter = KeyFilter(self.delete)
        self.widget.database_lists.installEventFilter(self.filter)
        self.database_info = {}

    def get(self,db_type):


        for db in range(self.widget.database_lists.count()):
            db_ = self.widget.database_lists.item(db).text()
            self.database_info[db_] = db_type

        return self.database_info

    def save(self,database,db_type):
        """
        save to database_lists
        """
        if database is list:
            for db in database:
                self.widget.database_lists.addItem(db)
                self.database_info[db] = db_type

        elif database is dict:
            for db,db_type1 in database:
                self.widget.database_lists.addItem(db)
                self.database_info[db] = db_type1
        else:
            self.widget.database_lists.addItem(database)
            self.database_info[database] = db_type

        
    def delete(self):

        selected = self.widget.database_lists.selectedItems()

        if not selected:
            QMessageBox.warning(self.widget,'warning','nothing is selected.',QMessageBox.StandardButton.Ok)
            return
        
        for item in selected:

            self.widget.database_lists.takeItem(
                self.widget.database_lists.row(item)
            )

    
  