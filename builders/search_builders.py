from config.config import searchConfigs
from managares.topic_manager import Topic
from managares.city_manager import City
from managares.database_manager import Database
from config.config import build_config,check_past_search


class BuildSearchConfig:

    def __init__(self, config):

        self.widget = config.window

        self.selected_cities = config.selected_cities

        self.minimum = config.minimum
        self.maximum = config.maximum
        self.name_value = config.name_value
        self.state_value = config.state_value

        self.manager_config = build_config(
            selected_cities=self.selected_cities
        )

        self.topic_manager = Topic(self.widget)
        self.city_manager = City(self.widget, self.manager_config)
        self.database_manager = Database(self.widget)

    def collect_search_data(self):
        database_name = []

        topics = self.topic_manager.collect()

        cities = {}

        for i in range(self.widget.added_cities.count()):
            city = self.widget.added_cities.item(i).text()
            cities[city] = self.selected_cities[city]

        for item in range(self.widget.database_lists.count()):

            database_name.append(self.widget.database_lists.item(item).text().strip())


        if self.widget.sqlite_radio.isChecked():
            database_type = 1

        if self.widget.csv_radio.isChecked():
            database_type = 2

        if self.widget.csv_radio.isChecked() and self.widget.sqlite_radio.isChecked():
            database_type = 3

        else:
            database_type = 3


        if not database_name:
            database_name = ["default_db"]

        filters = {}

        if self.widget.price_filter.isChecked():

            filters["price"] = {
                "minimum": self.minimum,
                "maximum": self.maximum
            }

        if self.widget.name_filter.isChecked():

            filters["name"] = self.name_value

        if self.widget.state_filter.isChecked():

            filters["state"] = self.state_value


        to_pst = check_past_search.topics
        to_cit = check_past_search.cities
        
        if to_cit and to_pst:
            if topics in to_pst and cities in to_cit:
                pass
            else:
                check_past_search(
                    topics=topics,
                    cities=cities
                )

        else:
            pass

        

        
        searchConfig = searchConfigs(
            topics=topics,
            cities=cities,
            database_name=database_name,
            database_type=database_type,
            filters=filters
        )

    
        return searchConfig 
    