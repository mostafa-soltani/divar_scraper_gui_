from services.check_past_search import Check_Past_search
from PySide6.QtWidgets import QMessageBox
from core.services import log
from config.past_search_config import past_search_search
import traceback

past_data = Check_Past_search()


class LoadPastSearch:
    def __init__(self,window):
        self.widget = window
        self.selected_cities = {}
        self.database_name = None
        self.database_type = None
        pass
    
    def get(self,logsignal):
        try:
            result = past_data.Past_Search()

            if result:
                reply = QMessageBox.question(
                    self.widget,
                    'Search History',
                    'Continue Previous Search?',
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )

                if reply == QMessageBox.StandardButton.Yes:
                    (
                        self.topic,
                        self.city,
                        self.city_id,
                        self.database_name,
                        self.database_type
                    ) = result

                    if isinstance(self.topic,list):
                        for topic in self.topic:
                            self.widget.topic_to_search.addItem(topic)

                    else:
                        self.widget.topic_to_search.addItem(self.topic)

                    if type(self.city) == dict:
                        for city,city_id in self.city.items():

                            self.widget.added_cities.addItem(city)

                            self.selected_cities[city] = city_id

                    if type(self.city) is list and type(self.city_id) is list:
                        for city,city_id in zip(self.city,self.city_id):
                            self.widget.added_cities.addItem(city)
                            self.selected_cities[city] = city_id


                    if type(self.database_name) is list:
                        for db in self.database_name:
                            self.widget.database_lists.addItem(db)

                    else:
                        self.widget.database_lists.addItem(self.database_name)
            else:
                return None
            

            logsignal.past_search.emit()
            
            return past_search_search(selected_cities=self.selected_cities, database_name=self.database_name,database_type=self.database_type)
        

        except Exception as e:
            traceback.print_exc()
            log.error_log(
                error=str(e),
                where='servises/load past search',
                state=None,
                error_file='databases/load_past_search.json'
            )