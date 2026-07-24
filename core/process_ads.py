import os
from core.services import stats,log,save,extractor
from storage.SQLite_database import SQLDatabase
from config.ad import Ad
import datetime


sql_database = SQLDatabase()

ad_ = Ad

class process_ads:
    """
    process ads is a class to process pages of data and ads and save the ads in databases who the user choose 
    """

    def __init__(self):
        self.city = None
        self.datetime = datetime.datetime.now().strftime('%Y/%M/%D:%H')
        pass

    def process(
            self,
            filters,
            page_json,
            database_name,
            database_type,
            cancel_token,
            state,
            url,
            signals,
            logsignal
            ):
        """
        process ads is a class to process pages of data and ads and save the ads in databases who the user choose.

        take data config, page_json,state,url

        data_config : all of data that needed for process inclode filter informations.
        page_json : the page that readed from site with connction.
        state : the status code from site for save in databases.
        url : for save in log.
        """

        filter_name = None
        minimum = None
        maximum = None
        name = None
        state = None
        page1 = 0

        if 'price' in filters:
            filter_name = 'price_filter'
            minimum = filters["price"]["minimum"]
            maximum = filters["price"]["maximum"]
        
        if 'name' in filters:
            filter_name = 'name_filter'
            name = filters["name"]
            minimum = None
            maximum = None

        if 'state' in filters:
            filter_name = 'state_filter'
            state = filters['state']
            minimum = None
            maximum = None
            
        if cancel_token.is_cancelled():
            signals.cancelled.emit()
            logsignal.cancelled.emit()

            return sql_database.close()
        
        ads_extracted = extractor.extract(
            data_json=page_json
        )

        stats.pagecount()
        

        self.database_name = database_name
        signals.current_city.connect(self.city_city)
        


        if ads_extracted:
            if cancel_token.is_cancelled():
                signals.cancelled.emit()
                logsignal.cancelled.emit()

                return

            if database_type == 1:
                data = []
                for p in ads_extracted:
                    row = [
                    p["title"],
                    self.city,
                    p["description"],
                    p["state"],
                    self.datetime
                    ]

                    page1 = p["current_page"]

                    data.append(row)


                signals.ads.emit(data)
                logsignal.current_page.emit(int(page1))

                self.__save_sql(ads_extracted,cancel_token,signals,logsignal)
                    

            if database_type == 2:
                data = []
                for p in ads_extracted:
                    row = [
                    p["title"],
                    self.city,
                    p["description"],
                    p["state"],
                    self.datetime
                    ]
                    page1 = p['current_page']


                    data.append(row)




                signals.ads.emit(data)
                logsignal.current_page.emit(int(page1))

                self.__save_csv(ads_extracted)

            if database_type == 3:
                data = []
                for p in ads_extracted:
                    row = [
                    p["title"],
                    self.city,
                    p["description"],
                    p["state"],
                    self.datetime
                    ]
                    page1 = p['current_page']


                    data.append(row)


                signals.ads.emit(data)
                logsignal.current_page.emit(int(page1))

                self.__save_sql(ads_extracted,cancel_token,signals,logsignal)
                self.__save_csv(ads_extracted)



            stats.adsfound(len(ads_extracted))

        level = "good" if state == 200 else "bad"

        log.readed_page(stats.page_count,stats.ads_found)

        signals.total_pages.emit(stats.page_count)

        signals.ad_found.emit(stats.ads_found)

        signals.ad_saved.emit(stats.ads_saved)

        signals.duplicate.emit(stats.ads_found - stats.ads_saved)

        log.connect_log(
                        conection=state,
                        level=level,
                        url=url,
                        database_name='databases/connect_log.json',
                        database_path=os.path.abspath('databases/connect_log.json')
                        )
        
        return sql_database
    
    def city_city(self,message):
        self.city = message


    def __save_sql(
            self,
            ads_extracted,
            cancel_token,
            signals,
            logsignal) -> None:

        try:
            

            if self.database_name != 'test':

                sql_database.create(self.database_name)

            else:

                sql_database.create(':memory:')


            sql_database.create_table()


            for item in ads_extracted:

                if cancel_token.is_cancelled():
                    signals.cancelled.emit()
                    logsignal.cancelled.emit()
                    return

                ad_config = ad_(
                    title=item['title'],
                    token=item["token"],
                    url=item["url"],
                    address=item["address"],
                    description=item["description"],
                    state=item["state"]
                )

                sql_database.insert(ad_config)


        except Exception as e:

            print(e)

            log.error_log(
                error=str(e),
                where='process_ads.process_ads.process',
                state=None
            )

    def __save_csv(self,ads_extracted) -> None:

        stats.adssaved(
            save.csv_database(
            self.database_name,
            ads_extracted
            )
                )
