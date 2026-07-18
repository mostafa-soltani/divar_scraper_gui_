from PySide6.QtWidgets import QMessageBox
from filters.ok_event import KeyFilter
import traceback

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

    def save(self):
        """
        save to database_lists
        """

        database = []

        database = self.widget.dataabse_name.text().strip()

        if not database:
            QMessageBox.critical(
                self.widget,
                'database name',
                'inter the database name and press this.',
                QMessageBox.StandardButton.Ok
            )

            return
        self.widget.dataabse_lists.addItem(database)
        self.widget.database_name.clear()

        

        
    def delete(self):

        selected = self.widget.database_lists.selectedItems()

        if not selected:
            QMessageBox.warning(self.widget,'warning','nothing is selected.',QMessageBox.StandardButton.Ok)
            return
        
        for item in selected:

            self.widget.database_lists.takeItem(
                self.widget.database_lists.row(item)
            )

    def add_item(self,db_name):
        if isinstance( db_name,list):
            for db in db_name:
                self.widget.database_lists.addItem(db)


        else:

            self.widget.database_lists.addItem(db_name)
  