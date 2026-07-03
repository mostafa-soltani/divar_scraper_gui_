from config.config import searchConfigs,config_api_data
from core.Cancel_token import CancelToken
from workers.search_worker import SearchWorker
from PySide6.QtCore import QThreadPool

api_config = config_api_data
search_config = searchConfigs

class SearchController:

    def __init__(self):
           
        self.pool = QThreadPool.globalInstance()
        self.cancel_token = CancelToken()

    def start(self,searchconfig):

        print('start_searchcontrol')
        worker = SearchWorker(searchconfig,self.cancel_token)

        self.pool.start(worker)


        return worker
    def cancel(self):
        self.cancel_token.cancel()