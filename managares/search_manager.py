from PySide6.QtWidgets import QMessageBox
from builders.search_builders import BuildSearchConfig
from config.config import build_config
from controllers.search_controller import SearchController
from managares.topic_manager import Topic
from managares.city_manager import City
from managares.status_manager import Status_Managers
from managares.log_manager import Log_manager


class Search_manager:
    def __init__(self,widget,logsignal) -> None:
        self.widget = widget
        self.log_signal = logsignal
        self.controller = SearchController()
        self.status_manager = Status_Managers(self.widget)


    def Start(
            self,
            c_config):
        if self.search:
            return
        
        self.search = True


        config = build_config(
            window=self.widget,
            selected_cities=c_config.selected_cities,
            minimum=c_config.minimum,
            maximum=c_config.maximum,
            name_value=c_config.name_value,
            state_value=c_config.state_value
        )

        self.searchconfig = BuildSearchConfig(config).collect_search_data()

        

        if self.searchconfig == self.last_search:
            QMessageBox.information(
                self.widget,
                'search',
                "this search has already been started"
            )
            return 

        worker = self.controller.start(
            searchconfig=self.searchconfig,
            log_signal = self.log_signal
            )
        

        self.last_search = self.searchconfig

        

        topics = Topic(self.widget).collect()
        cities = City(self.widget,config=config).collect()

        for topic,city in zip(topics,cities):

            self.widget.topics_status.addItem(topic)
            self.widget.cities_status.addItem(city)



        worker.signals.progress.connect(
            self.widget.progressBar.setValue
        )

        worker.signals.current_topic.connect(
            self.status_manager.update_topic
        )

        worker.signals.current_city.connect(
            self.status_manager.update_city
        )


        worker.signals.current_database.connect(
            self.status_manager.update_database
        )

        worker.signals.page.connect(
            self.status_manager.page_num
        )

        worker.signals.ad_found.connect(
            self.status_manager.ad_found
        )
        worker.signals.ad_saved.connect(
            self.status_manager.ad_saved
        )

        worker.signals.duplicate.connect(
            self.status_manager.duplicate
        )
 

        worker.signals.cancelled.connect(
            self.status_manager.search_cancelled
        )

        worker.signals.finished.connect(
            self.status_manager.search_finished
        )

        worker.signals.error.connect(
            self.status_manager.show_error
        )

        worker.signals.ads.connect(self.status_manager.ads_table)
        
        self.widget.cancel.clicked.connect(self.controller.cancel)


        self.search = False