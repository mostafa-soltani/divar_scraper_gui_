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

past_search = Check_Past_search()
find_city = CityResolver()

class MainWindow:
    def __init__(self):
        self._load_ui()
        self._init_variables()
        self._ui_chenge()
        self._hide_frame()
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





    def _load_ui(self):
        loader = QUiLoader()

        file = QFile('gui/ui_ui.ui')

        file.open(QFile.ReadOnly)

        self.window = loader.load(file)

        file.close()

    def _ui_chenge(self):
        

        self.filter_group = QButtonGroup(self.window)

        self.filter_group.addButton(self.window.yes_filter)
        self.filter_group.addButton(self.window.no_filter)

        self.filter_group.setExclusive(True)

    def _hide_frame(self):

        for frame in (
            self.window.filter_frame,
            self.window.price_frame,
            self.window.name_frame,
            self.window.state_frame
        ):
            frame.hide()


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
                    _,
                    self.database_name,
                    self.database_type,
                ) = result


                if isinstance(self.topic,list):
                    for topic in self.topic:
                        self.window.topic_to_search.addItem(topic)
                else:
                    self.window.topic_to_search.addItem(self.topic)
                for city,city_id in self.city.items():

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

        self.window.choose_city.clicked.connect(self.choose_city)
        self.window.search_button.clicked.connect(self.start_search)

        self.window.yes_filter.toggled.connect(self.filter_yes)
        self.window.no_filter.toggled.connect(self.filter_no)
        self.window.price_filter.toggled.connect(self.price_panle)
        self.window.name_filter.toggled.connect(self.name_panle)
        self.window.state_filter.toggled.connect(self.state_panle)

    def topic_save(self):
        topic = self.window.topic.text().strip().lower()

        if not topic:
            QMessageBox.warning(self.window,'warning','the topic section is empty',QMessageBox.StandardButton.Ok)
            return
        
        self.window.topic_to_search.addItem(topic)
        self.window.topic.clear()

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


    def filter_yes(self,checked):
        self.window.filter_frame.setVisible(checked)
        '''self.window.price_frame.hide()
        self.window.name_frame.hide()
        self.window.state_frame.hide()'''
        return checked
    def filter_no(self,checked):
        self.window.filter_frame.setVisible(False)
        self.window.price_frame.hide()
        self.window.name_frame.hide()
        self.window.state_frame.hide()
    
    def price_panle(self,checked):

        self.window.price_frame.setVisible(checked)

        if checked:
            self.window.name_frame.hide()
            self.window.state_frame.hide()
            self.window.price_save.clicked.connect(self.min_max_saver)

        
    def name_panle(self,checked):

        self.window.name_frame.setVisible(checked)

        if checked:
            self.window.price_frame.hide()
            self.window.state_frame.hide()
            self.window.name_save.clicked.connect(self.name_saver)

    def name_saver(self):

        self.value = self.window.name_str.text().strip().lower()

    def state_panle(self,chekced):

        self.window.state_frame.setVisible(chekced)

        if chekced:
            self.window.price_frame.hide()
            self.window.name_frame.hide()
            self.window.state_save.clicked.connect(self.state_saver)

    def state_saver(self):
        
        self.value = self.window.state_str.text().strip().lower()


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