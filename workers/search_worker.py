from core.request_api import ApiRequest
from PySide6.QtCore import QRunnable,Slot
from signals.signals import WorkerSignals
from config.config import config_api_data
import datetime


class SearchWorker(QRunnable):
    def __init__(
            self,
            search_config,
            cancel_token,
            log_signal
            ) -> None:
        super().__init__()

        print('start_search_worker')

        self.request = ApiRequest()
        self.signals = WorkerSignals()
        self.search_config = search_config
        self.api_config = config_api_data()
        self.log_signal = log_signal
        self.url = self.api_config.url
        self.cancel_token = cancel_token
        self.filters = search_config.filters
        self.database_name = search_config.database_name
        self.database_type = search_config.database_type
        
            
    @Slot()
    def run(self):
        try:
            time_start = datetime.datetime.now()

            self.request.request(
                url=self.url,
                search_config=self.search_config,
                time_start=time_start,
                signals=self.signals,
                cancel_token = self.cancel_token,
                filters=self.filters,
                database_name=self.database_name,
                database_type=self.database_type,
                log_signal = self.log_signal
                )
            
            if self.cancel_token.is_cancelled():
                self.signals.cancelled.emit()
                return
                    

        except Exception as e:
            self.signals.error.emit(str(e))