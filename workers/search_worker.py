from core.request_api import ApiRequest
from PySide6.QtCore import QRunnable,Slot
from signals.signals import WorkerSignals
from config.config import config_api_data
import datetime


class SearchWorker(QRunnable):
    def __init__(self,search_config,cancel_token) -> None:
        super().__init__()

        print('start_search_worker')

        self.request = ApiRequest()
        self.signals = WorkerSignals()
        self.search_config = search_config
        self.api_config = config_api_data()
        self.url = self.api_config.url
        self.cancel_token = cancel_token
        
            
    @Slot()
    def run(self):
        try:
            time_start = datetime.datetime.now()

            self.request.request(
                url=self.url,
                search_config=self.search_config,
                time_start=time_start,
                signals=self.signals,
                cancel_token = self.cancel_token
                )
                    
            self.signals.finished.emit()

        except Exception as e:
            self.signals.error.emit(str(e))