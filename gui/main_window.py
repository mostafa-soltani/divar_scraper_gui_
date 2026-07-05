from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from services.check_past_search import Check_Past_search
from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtCore import QRegularExpression
from PySide6.QtWidgets import QProgressDialog
from PySide6.QtWidgets import QButtonGroup
from storage.city_resolver import CityResolver
from controllers.search_controller import SearchController
from config.config import searchConfigs
from logs.log import log_data


past_search = Check_Past_search()
find_city = CityResolver()
log = log_data()

class MainWindow:
    def __init__(self):
        self._load_ui()
        self._init_variables()
        self._load_past_search()
        self._setup_validators()
        self._connect_signals()

    def _init_variables(self):
        self.topics = []
        self.cities = {}
        self.loaded_cities = set()
        self.selected_cities = {}
        self.value = None
        self.database_type = 2
        self.searchconfig = None
        self.controller = SearchController()
        self.search = False
        self.database_name = None
        self.database_type = None





    def _load_ui(self):
        loader = QUiLoader()

        file = QFile('new_ui/new.ui')

        file.open(QFile.ReadOnly)

        self.window = loader.load(file)

        file.close()




    def _load_past_search(self):
        result = past_search.Past_Search()

        if result:
            reply = QMessageBox.question(
                self.window,
                "Search History",
                "Continue previous search?",
                QMessageBox.Yes | QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                (
                    self.topic,
                    self.city,
                    self.city_id,
                    self.database_name,
                    self.database_type,
                ) = result


                if isinstance(self.topic,list):
                    for topic in self.topic:
                        self.window.topic_to_search.addItem(topic)
                else:
                    self.window.topic_to_search.addItem(self.topic)

                if type(self.city) == dict:
                    for city,city_id in self.city.items():

                        self.window.added_cities.addItem(city)
                        self.selected_cities[city] = city_id
                if type(self.city) is list and type(self.city_id) is list:
                    for city,city_id in zip(self.city,self.city_id):
                        self.window.added_cities.addItem(city)
                        self.selected_cities[city] = city_id
                    
                self.window.database_name.setText(self.database_name)

        else:
            pass


    def _setup_validators(self):

        validator = QRegularExpressionValidator(
            QRegularExpression(r"\d{1,15}")
        )


        for item in (
            self.window.minimum_price,
            self.window.maximum_price
        ):
            item.setValidator(validator)

    def _connect_signals(self):
        self.window.topic.returnPressed.connect(self.topic_save)
        self.window.city.returnPressed.connect(self.city_save)

        self.window.topic_save.clicked.connect(self.topic_save)
        self.window.city_save.clicked.connect(self.city_save)
        self.window.save_database.clicked.connect(self.database_save)

        self.window.choose_city.clicked.connect(self.choose_city)
        self.window.search_button.clicked.connect(self.start_search)

        self.window.price_filter.toggled.connect(self.price_panle)
        self.window.name_filter.toggled.connect(self.name_panle)
        self.window.state_filter.toggled.connect(self.state_panle)

        self.window.delete_topic.clicked.connect(self.delete_topic)
        self.window.delete_city.clicked.connect(self.delete_city)
        self.window.delete_database_item.clicked.connect(self.delete_database_name)
        

    def topic_save(self):
        topic = self.window.topic.text().strip().lower()

        if not topic:
            QMessageBox.warning(self.window,'warning','the topic section is empty',QMessageBox.StandardButton.Ok)
            return
        
        self.window.topic_to_search.addItem(topic)
        self.window.topic.clear()

    def database_save(self):

        database_name = self.window.database_name.text().strip().lower()

        if not database_name:
            QMessageBox.warning(self.window,'warning','the database section is empty',QMessageBox.StandardButton.Ok)
            return
        
        self.window.database_lists.addItem(database_name)
        self.window.database_name.clear()

    def _city_search(self, city):
        new_cities = find_city.get_city_ids(city)


        if not new_cities:
            QMessageBox.warning(
                self.window,
                "Warning",
                "The city section is empty.",
                QMessageBox.StandardButton.Ok,
            )
            return
        
        for city_name, city_id in new_cities.items():
            if city_name not in self.loaded_cities:
                self.loaded_cities.add(city_name)
                self.window.founded_cities.addItem(city_name)

            elif city_name in self.selected_cities.keys():

                self.selected_cities.update(new_cities)

            self.selected_cities[city_name] = city_id

    def city_save(self):

        city = self.window.city.text().strip().lower()

        if not city:
            QMessageBox.warning(self.window,'warning','the topic section is empty',QMessageBox.StandardButton.Ok)

        self._city_search(city)
        self.window.city.clear()

    def choose_city(self):

        selected = self.window.founded_cities.selectedItems()

        if not selected:
            QMessageBox.warning(self.window,'warning','nothing selected.',QMessageBox.StandardButton.Ok)

        for city in selected:
            self.window.added_cities.addItem(city.text().lower())
            self.window.founded_cities.takeItem(
                self.window.founded_cities.row(city)
            )




    def min_max_saver(self):

        minimum = self.window.minimum_price.text().strip()
        maximum = self.window.maximum_price.text().strip()

        if not minimum and not maximum:
            QMessageBox.warning(
                self.window,
                "Price Filter",
                "Please enter at least one price."
            )
            return

        self.minimum = int(minimum) if minimum else 0
        self.maximum = int(maximum) if maximum else 1_000_000_000_000_000

    
    def price_panle(self):

        self.window.price_save.clicked.connect(self.min_max_saver)

        
    def name_panle(self):

        self.window.name_save.clicked.connect(self.name_saver)

    def name_saver(self):

        self.value = self.window.name_str.text().strip().lower()

    def state_panle(self,chekced):


        self.window.state_save.clicked.connect(self.state_saver)

    def state_saver(self):
        
        self.value = self.window.state_str.text().strip().lower()


    def delete_city(self):
        selected = self.window.added_cities.selectedItems()

        if not selected:
            QMessageBox.warning(self.window,'warning','nothing selected.',QMessageBox.StandardButton.Ok)
            return
        
        for topic in selected:

            self.window.added_cities.takeItem(
                self.window.added_cities.row(topic)
            )

    def delete_database_name(self):
        selected = self.window.database_lists.selectedItems()

        if not selected:
            QMessageBox.warning(self.window,'warning','nothing selected.',QMessageBox.StandardButton.Ok)
            return

        for database_name in selected:

            self.window.database_lists.takeItem(
                self.window.database_lists.row(database_name)
            )

    def delete_topic(self):
        selected = self.window.topic_to_search.selectedItems()

        if not selected:
            QMessageBox.warning(self.window,'warning','nothing selected.',QMessageBox.StandardButton.Ok)
            return

        for database_name in selected:

            self.window.topic_to_search.takeItem(
                self.window.topic_to_search.row(database_name)
            )




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

    def search_finished(self):
        self.progress.close()
        self.search = False

        QMessageBox.information(
            self.window,
            "Done",
            "Search completed successfully."
        )
        

    def show_error(self, message):
        self.progress.close()
        self.search = False

        QMessageBox.critical(
            self.window,
            "Error",
            message
        )

    def start_search(self):
        
        log.search_log(topic=self.topics,
                                  city=list(self.cities.keys()),
                                  city_ids=list(self.cities.values()),
                                  database_name=self.database_name,
                                  database_type=self.database_type)

        if not self.search:

            self.collect_search_data()

            self.progress = QProgressDialog(
            "Searching...",
            None,
            0,
            100,
            self.window
            )

            self.progress.setWindowTitle("Divar Scraper")
            self.progress.setCancelButtonText('cancel')
            self.progress.setAutoClose(False)
            self.progress.setAutoReset(False)

            self.progress.show()

            worker = self.controller.start(searchconfig=self.searchconfig)
            self.progress.show()
            worker.signals.progress.connect(self.progress.setValue)
            self.progress.canceled.connect(self.controller.cancel)
            worker.signals.finished.connect(self.search_finished)
            worker.signals.error.connect(self.show_error)

            if worker is not None:
                self.search = True

            else:
                self.search = False