from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtCore import QRegularExpression
from services.load_past_search import LoadPastSearch
from controllers.search_controller import SearchController
from config.config import build_config
from storage.city_resolver import CityResolver
from filters.min_max_filter import Set_Min_Max
from builders.search_builders import BuildSearchConfig
from ui_managares.topic_manager import Topic
from ui_managares.city_manager import City
from ui_managares.database_manager import Database
from filters.City_list_event import CityListFilter
from models.ads_model import AdsModel

find_city = CityResolver()

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
            self.city = None
            self.controller = SearchController()
            self.manager_config = build_config(
                selected_cities=self.selected_cities
            )
            self.topic_manager = Topic(self.window)
            self.city_manager = City(self.window,self.manager_config)
            self.database_manager = Database(self.window)
            self.city_filter = CityListFilter(self,self.city_manager)
            self.past_search = LoadPastSearch(self.window)
            self.set_min_max = Set_Min_Max(self.window)
            self.model = AdsModel([])

            self.window.ads_table.setModel(self.model)

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

        config = self.past_search.get()

        if config:

            self.selected_cities = config.selected_cities

            self.database_manager.save(database=config.database_name,db_type=config.database_type)
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
        self.window.city.returnPressed.connect(self.selected_cities_func)
        self.window.database_name.returnPressed.connect(self.database_save)


        self.window.topic_save.clicked.connect(self.topic_save)
        self.window.city_save.clicked.connect(self.selected_cities_func)
        self.window.save_database.clicked.connect(self.database_save)

        self.window.choose_city.clicked.connect(lambda :self.city_manager.choose_city())
        self.window.search_button.clicked.connect(self.start_search)

        self.window.price_filter.toggled.connect(self.price_panle)
        self.window.name_filter.toggled.connect(self.name_panle)
        self.window.state_filter.toggled.connect(self.state_panle)

        self.window.delete_city.clicked.connect(
            lambda : self.city_manager.delete()
            )

        self.window.delete_topic.clicked.connect(
            lambda: self.topic_manager.delete()
            )

        self.window.delete_database_item.clicked.connect(
            lambda: self.database_manager.delete()
            )
        
    def selected_cities_func(self):
        self.selected_cities = self.city_manager.add_city()

        
    def topic_save(self):

        self.topic_manager.save()
        
    def database_save(self):

        database_name = self.window.database_name.text().strip().lower()

        if not database_name:
            QMessageBox.warning(self.window,'warning','the database section is empty',QMessageBox.StandardButton.Ok)
            return
        
        self.window.database_lists.addItem(database_name)
        self.window.database_name.clear()


    def ads_table(self,data):

        self.model._data.extend(data)

        self.model.layoutChanged.emit()
            
    

    def min_max_saver(self):

        self.minimum,self.maximum = self.set_min_max.set_price()
    
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

    def update_topic(self, topic):

        self.window.current_topic.setText(topic)

    def update_city(self, city):

        self.window.current_city.setText(city)

    def duplicate(self,message):
        
        self.window.duplicate.setText(message)


    def update_database(self, database):

        self.window.current_db_name.setText(database)

    def connection_status(self,message):
        self.window.current_state.setText(str(message))

    def page_num(self,message):
        self.window.current_page.setText(str(message))

    def ad_found(self,message):
        self.window.ads_found.setText(str(message))

    def ad_saved(self,message):
        self.window.ads_saved.setText(str(message))




    def search_finished(self):
        QMessageBox.information(
            self.window,
            "Done",
            "Search completed."
        )

    def search_cancelled(self):
        QMessageBox.information(
            self.window,
            "Cancelled",
            "Search cancelled."
        )

    def show_error(self, message):
        QMessageBox.critical(
            self.window,
            "Error",
            message
        )



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
        

        self.last_search = self.searchconfig

        

        topics = Topic(self.window).collect()
        cities = City(self.window,config=config).collect()

        for topic,city in zip(topics,cities):

            self.window.topics_status.addItem(topic)
            self.window.cities_status.addItem(city)



        worker.signals.progress.connect(
            self.window.progressBar.setValue
        )

        worker.signals.current_topic.connect(
            self.update_topic
        )

        worker.signals.current_city.connect(
            self.update_city
        )


        worker.signals.current_database.connect(
            self.update_database
        )

        worker.signals.page.connect(
            self.page_num
        )

        worker.signals.ad_found.connect(
            self.ad_found
        )
        worker.signals.ad_saved.connect(
            self.ad_saved
        )

        worker.signals.duplicate.connect(
            self.duplicate
        )
 

        worker.signals.finished.connect(
            self.search_finished
        )

        worker.signals.cancelled.connect(
            self.search_cancelled
        )

        worker.signals.error.connect(
            self.show_error
        )

        worker.signals.ads.connect(self.ads_table)
        
        self.window.cancel.clicked.connect(self.controller.cancel)
        worker.signals.cancelled.connect(self.search_cancelled)
        worker.signals.finished.connect(self.search_finished)
        worker.signals.error.connect(self.show_error)
