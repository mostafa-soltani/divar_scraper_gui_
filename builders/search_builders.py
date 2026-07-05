from config.config import searchConfigs

class build_search_config:

    def __init__(self,window, selected_cities,minimum,maximum,value) -> None:
        self.window = window
        self.topics = []
        self.cities = {}
        self.selected_cities = selected_cities
        self.minimum = minimum
        self.maximum = maximum
        self.value = value
    def collect_search_data(self):
        for topic_num in range(self.window.topic_to_search.count()):
            self.topics.append(self.window.topic_to_search.item(topic_num).text())

        for city_num in range(self.window.added_cities.count()):
            city = self.window.added_cities.item(city_num).text()
            self.cities[city] = self.selected_cities[city]

        self.database_name = self.window.database_name.text()

        if self.window.sqlite_radio.isChecked():
            self.database_type = 1

        else:
            self.database_type = 2

        if not self.database_name and not self.database_type:
            self.database_type,self.database_name = 2,'defult_db'

        if self.window.yes_filter.isChecked():
            if self.window.price_filter.isChecked():
                filter_name = 'price filter'
                filter_value = None
                min_ = self.minimum
                max_ = self.maximum

            elif self.window.name_filter.isChecked():
                filter_name = 'name filter'
                filter_value = self.value
                min_ = None
                max_ = None

            elif self.window.state_filter.isChecked():
                filter_name = 'state filter'
                filter_value = self.value
                min_ = None
                max_ = None

        else:
            filter_name = None
            filter_value = None
            min_ = None
            max_ = None

        self.searchconfig = searchConfigs(
            topics = self.topics,
            cities = self.cities,
            database_name=self.database_name,
            database_type=self.database_type,
            filter_name=filter_name,
            filter_value=filter_value,
            minimum_price=min_,
            maximum_price=max_
        )

        return self.searchconfig
    
