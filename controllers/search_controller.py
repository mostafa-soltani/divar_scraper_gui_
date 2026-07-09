from config.config import searchConfigs,config_api_data
from core.Cancel_token import CancelToken
from workers.search_worker import SearchWorker
from PySide6.QtCore import QThreadPool
from logs.log import log_data

api_config = config_api_data
search_config = searchConfigs
log = log_data()

class SearchController:

    def __init__(self):
           
        self.pool = QThreadPool.globalInstance()
        self.cancel_token = CancelToken()

    def start(
            self,
            searchconfig):

        log.search_log(
            topic=searchconfig.topics,
            city=list(searchconfig.cities.keys()),
            city_ids=list(searchconfig.cities.values()),
            database_name=searchconfig.database_name,
            database_type=searchconfig.database_type
        )

        self.cancel_token.reset()

        print('start_searchcontrol')
        worker = SearchWorker(
            searchconfig,
            self.cancel_token)
        
        

        self.pool.start(worker)


        return worker
    

    def cancel(self):
        self.cancel_token.cancel()