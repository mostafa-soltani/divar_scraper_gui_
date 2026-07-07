from config.config import searchConfigs
from ui_managares.topic_manager import Topic
from ui_managares.city_manager import City
from ui_managares.database_manager import Database
from config.config import build_config


class BuildSearchConfig:

    def __init__(self, config):

        self.window = config.window

        self.selected_cities = config.selected_cities

        self.minimum = config.minimum
        self.maximum = config.maximum
        self.value = config.value

        self.manager_config = build_config(
            selected_cities=self.selected_cities
        )

        self.topic_manager = Topic(self.window)
        self.city_manager = City(self.window, self.manager_config)
        self.database_manager = Database(self.window)

    def collect_search_data(self):
        database_name = []

        topics = self.topic_manager.collect()

        cities = {}

        for i in range(self.window.added_cities.count()):
            city = self.window.added_cities.item(i).text()
            cities[city] = self.selected_cities[city]

        for item in range(self.window.database_lists.count()):

            database_name.append(self.window.database_lists.item(item).text().strip())

        database_type = 1 if self.window.sqlite_radio.isChecked() else 2

        if not database_name:
            database_name = ["default_db"]

        filters = {}

        if self.window.price_filter.isChecked():

            filters["price"] = {
                "minimum": self.minimum,
                "maximum": self.maximum
            }

        if self.window.name_filter.isChecked():

            filters["name"] = self.value

        if self.window.state_filter.isChecked():

            filters["state"] = self.value


        print(topics,' + ', cities , ' + ', database_name , " + ", database_type , " + ", filters)

        
        searchConfig = searchConfigs(
            topics=topics,
            cities=cities,
            database_name=database_name,
            database_type=database_type,
            filters=filters
        )

        print(searchConfig)
    
        return searchConfig 
    