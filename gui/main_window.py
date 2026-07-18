from PySide6.QtWidgets import QMessageBox
from services.load_past_search import LoadPastSearch
from controllers.search_controller import SearchController
from config.config import c_config,build_config
from storage.city_resolver import CityResolver
from filters.min_max_filter import Set_Min_Max
from managares.topic_manager import Topic
from managares.city_manager import City
from managares.database_manager import Database
from filters.City_list_event import CityListFilter
from core.ui_loader import Load_Ui
from core.Validators_Setup import Validator_price
from managares.search_manager import Search_manager
from signals.signals import LogSignals
from managares.filter_manager import Filter_Manager
from managares.log_manager import Log_manager


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
            self.name_value = None
            self.state_value = None
            self.searchconfig = None
            self.search = False
            self.minimum = None
            self.maximum = None
            self.database_name = None
            self.logsignal = LogSignals()
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
            self.ui = Load_Ui('new_ui/new.ui')
            self.validator = Validator_price(self.window)
            self.searcher = Search_manager(self.window,self.logsignal)
            self.filter_manager = Filter_Manager(self.window)
            self.log_manager = Log_manager(self.window,log_signal=self.logsignal)




            self.window.founded_cities.installEventFilter(self.city_filter)
            self.window.added_cities.installEventFilter(self.city_filter)
        except Exception as e:
            print(e)
    def _load_ui(self):
        self.window = self.ui.load_ui(self.logsignal)

    def _load_past_search(self):

        config = self.past_search.get(self.logsignal)

        if config:

            self.selected_cities = config.selected_cities

            self.database_manager.add_item(db_name=config.database_name)
        else:
            pass

    def _setup_validators(self):
        self.validator.setup()

    def _log_satus(self):
        self.log_manager.show_log()
        

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

        self.database_manager.save()

        database_name = self.window.database_name.text().strip().lower()

        if not database_name:
            QMessageBox.warning(self.window,'warning','the database section is empty',QMessageBox.StandardButton.Ok)
            return
        
        self.window.database_lists.addItem(database_name)
        self.window.database_name.clear()


    

    def min_max_saver(self):
        self.minimum,self.maximum = self.filter_manager.get_price()
    
    def price_panle(self):
        self.window.price_save.clicked.connect(self.min_max_saver)

    def name_panle(self):
        self.window.name_save.clicked.connect(self.name_saver)

    def name_saver(self):
        self.name_value = self.filter_manager.get_name()

    def state_panle(self):
        self.window.state_save.clicked.connect(self.state_saver)

    def state_saver(self):
        self.state_value = self.filter_manager.get_state()




    def start_search(self):
        config = c_config(
            selected_cities=self.selected_cities,
            minimum=self.minimum,
            maximum=self.maximum,
            state_value=self.state_value,
            name_value=self.name_value
        )
        self.searcher.Start(c_config=config)
        
