import time
import datetime
from config.config import Data_Config
from colorama import init
from PySide6.QtCore import QObject, Signal
from core.HTTP_CLIENT import Paginator
from core.process_ads import process_ads
from core.request_client import RequestClient
from config.config import config_api_data,info
from logs.report import Report
from core.services import log,stats
import traceback


init()

client = RequestClient()
config = config_api_data()
processor = process_ads()
report = Report()




class ApiRequest:

    def __init__(self):
        self.state = None
        self.max_retry = config.max_retry


    def request(
        self,
        url,
        search_config,
        time_start,
        signals,
        cancel_token,
        filters,
        database_name,
        database_type
    ):
        
        """
        make the actual cinnection with sending request to site and use paginator and send data to process

        take url,data_config,timeout,report_config,payloads,headers

        url : the api url to make a connection.
        data_config : for usage in process data.
        timeout  : for usage in paginator.
        topics : list of all topics to search.
        cities : send a dict of cities and cities id.
        report_config : the config for report in final.
        headers : the search information for users to get what is the request sender.
        """


        try:

            topics = search_config.topics


            cities = search_config.cities


            headers = config.headers


            timeout = config.timeout
        except Exception as e:
            signals.error.emit(e)
            traceback.print_exc()
            raise


        print(topics[0:3],cities,headers,timeout)

        total = len(topics) * len(cities)

        current = 0


        try:

            if cancel_token.is_cancelled():
                signals.cancelled.emit()
                return

            for city, city_id in cities.items():
                if cancel_token.is_cancelled():
                    signals.cancelled.emit()
                    return


                for topic in topics:
                    if cancel_token.is_cancelled():
                        signals.cancelled.emit()
                        return

                    for retry in range(self.max_retry):
                        if cancel_token.is_cancelled():
                            signals.cancelled.emit()
                            return

                        current += 1

                        percent = int(current / total * 100 )

                        report_config = info(
                            topic=topic,
                            city=city,
                            time_start=time_start
                        )

                    


                        try:
                            print('trying')

                            signals.current_topic.emit(topic)
                            signals.current_city.emit(city)
                            signals.current_database.emit(database_name)
                            
                            paginator = self._create_paginator(
                                url=url,
                                headers=headers,
                                timeout=timeout,
                                city_id=city_id,
                                cancel_token=cancel_token,
                                topic=topic,
                            )



                            self._process_pages(
                                paginator=paginator,
                                url=url,
                                report_config=report_config,
                                filters=filters,
                                database_name=database_name,
                                cancel_token=cancel_token,
                                database_type=database_type
                            )

                            self.finals_log(database_name,topic,city)


                            signals.progress.emit(percent)
                            break

                        except Exception as e:

                            traceback.print_exc()

                            self._log_error(e)

                            if retry + 1 == self.max_retry:
                                print(f"Skip -> {city} | {topic}")

                            time.sleep(3)

                    
                    
            signals.finished.emit()

            return
        except Exception as e:
            print(e)

    def _build_payload(self, city_id, topic):

        return {
            "city_ids": [city_id],
            "source_view": "SEARCH",
            "disable_recommendation": False,
            "search_data": {
                "query": topic,
            },
        }

    def _create_paginator(
        self,
        url,
        headers,
        cancel_token,
        timeout,
        city_id,
        topic,
    ):

        return Paginator(
            client=client,
            url=url,
            headers=headers,
            payloads=self._build_payload(city_id, topic),
            cancel_token = cancel_token,
            timeout=timeout
        )

    def _process_pages(
        self,
        paginator,
        url,
        filters,
        report_config,
        database_name,
        cancel_token,
        database_type
    ):

        database = None

        for page_json, self.state in paginator:

            if report_config:
                self._update_report(report_config)

            database = processor.process(
                filters = filters,
                page_json=page_json,
                database_name=database_name,
                database_type=database_type,
                state=self.state,
                cancel_token = cancel_token,
                url=url,
            )

        if database:
            database.close()

    def _update_report(self, report_config):

        runtime = datetime.datetime.now() - report_config.time_start

        report.report_final(
            report_config.topic,
            report_config.city,
            str(runtime).split(".")[0],
        )

    def finals_log(self,database_name,topic,city):

        log.final_log(
            database_name=database_name,
            ads_found=stats.ads_found,
            ads_saved=stats.ads_saved,
            topic = topic,
            city=city
        )

    def _log_error(self, error):

        print(error)

        log.error_log(
            error=str(error),
            where="ApiRequest.request",
            state=self.state,
        )