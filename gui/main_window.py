from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtCore import QRegularExpression
from controllers.search_controller import SearchController
from config.config import build_config
from storage.city_resolver import CityResolver
from services.check_past_search import Check_Past_search
from builders.search_builders import BuildSearchConfig
from ui_managares.topic_manager import Topic
from ui_managares.city_manager import City
from ui_managares.database_manager import Database
from filters.City_list_event import CityListFilter
from gui.progress_dialog import Progress

find_city = CityResolver()
past_search = Check_Past_search()
class MainWindow:
    def __init__(self):
        self._load_ui()

        self._init_variables()

        self._load_past_search()

        self._setup_validators()

        self._connect_signals()

    
    def _init_variables(self):
        try:

            self.loaded_cities = set()
            self.selected_cities = {}
            self.value = None
            self.searchconfig = None
            self.search = False
            self.minimum = None
            self.maximum = None
            self.last_search = None
            self.controller = SearchController()
            self.manager_config = build_config(
                selected_cities=self.selected_cities
            )
            self.topic_manager = Topic(self.window)
            self.city_manager = City(self.window,self.manager_config)
            self.database_manager = Database(self.window)
            self.city_filter = CityListFilter(self)

            self.window.founded_cities.installEventFilter(self.city_filter)
            self.window.added_cities.installEventFilter(self.city_filter)
        except Exception as e:
            print(e)
    def _load_ui(self):
        loader = QUiLoader()

        file = QFile('new_ui/new.ui')

        file.open(QFile.ReadOnly)

        self.window = loader.load(file)

        file.close()




    def _load_past_search(self):
        try:
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

        except Exception as e:
            print(e)


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
        self.window.database_name.returnPressed.connect(self.database_save)


        self.window.topic_save.clicked.connect(self.topic_save)
        self.window.city_save.clicked.connect(self.city_save)
        self.window.save_database.clicked.connect(self.database_save)

        self.window.choose_city.clicked.connect(self.choose_city)
        self.window.search_button.clicked.connect(self.start_search)

        self.window.price_filter.toggled.connect(self.price_panle)
        self.window.name_filter.toggled.connect(self.name_panle)
        self.window.state_filter.toggled.connect(self.state_panle)

        self.window.delete_city.clicked.connect(
            lambda : self.delete_city()
            )

        self.window.delete_topic.clicked.connect(
            lambda: self.topic_manager.delete()
            )

        self.window.delete_database_item.clicked.connect(
            lambda: self.database_manager.delete()
            )
        
    def delete_city(self):
        self.city_manager.delete()

    def unchoose_city(self):
        self.city_manager.unchoose_city()
    
        
    def topic_save(self):

        self.topic_manager.save()
        
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

    def state_panle(self):

        self.window.state_save.clicked.connect(self.state_saver)

    def state_saver(self):
        
        self.value = self.window.state_str.text().strip().lower()




    def start_search(self):

        if self.search:
            return
        
        self.search = True

        config = build_config(
            window=self.window,
            selected_cities=self.selected_cities,
            minimum=self.minimum,
            maximum=self.maximum,
            value=self.value
        )

        self.searchconfig = BuildSearchConfig(config).collect_search_data()

        

        if self.searchconfig == self.last_search:
            QMessageBox.information(
                self.window,
                'search',
                "this search has already been started"
            )
            return 

        worker = self.controller.start(
            searchconfig=self.searchconfig)
        
        self.window.cancel.clicked.connect(self.controller.cancel)

        self.last_search = self.searchconfig

        

        topics = Topic(self.window).collect()
        cities = City(self.window,config=config).collect()

        for topic,city in zip(topics,cities):

            self.window.topic_status.addItem(topic)
            self.window.cities_status.addItem(city)

        info_page = Progress(self.window,worker)

        info_page.setup()

        worker.signals.cancelled.connect(info_page.search_cancelled)
        worker.signals.finished.connect(info_page.search_finished)
        worker.signals.error.connect(info_page.show_error)
