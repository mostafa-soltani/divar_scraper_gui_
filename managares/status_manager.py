
from PySide6.QtWidgets import QMessageBox
from managares.table_manager import TableManager



class Status_Managers:
    def __init__(self,widget):
        self.widget = widget
        self.model = TableManager(self.widget.ads_table)

    def update_topic(self, topic):

        self.widget.current_topic.setText(topic)

    def update_city(self, city):

        self.widget.current_city.setText(city)

    def duplicate(self,message):
        
        self.widget.duplicate.setText(str(message))

    def update_database(self, database):

        self.widget.current_db_name.setText(database)

    def connection_status(self,message):
        self.widget.current_state.setText(str(message))

    def page_num(self,message):
        self.widget.current_page.setText(str(message))

    def ad_found(self,message):
        self.widget.ads_found.setText(str(message))

    def ad_saved(self,message):
        self.widget.ads_saved.setText(str(message))

    def ads_table(self,data):
        self.model.add_ads(data)


    def search_finished(self):
        self.search = False

        self.minimum = None
        self.maximum = None
        self.name_value = None
        self.state_value = None


        QMessageBox.information(
            self.widget,
            "Done",
            "Search completed."
        )

    def search_cancelled(self):
        self.search = False

        self.minimum = None
        self.maximum = None
        self.name_value = None
        self.state_value = None

        QMessageBox.information(
            self.widget,
            "Cancelled",
            "Search cancelled."
        )

    def show_error(self, message):
        self.search = False
        QMessageBox.critical(
            self.widget,
            "Error",
            message
        )