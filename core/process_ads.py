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
        self.datetime = datetime.datetime.now().strftime('%Y/%M/%D/%H :%m :%S')
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
            signals
            ) -> object:
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
            return
        
        page = extractor.extract(
            data_json=page_json,
            filter_name=filter_name,
            min_price=minimum,
            max_price=maximum,
            name_filter=name,
            state_filter=state
        )

        stats.pagecount()
        

        self.database_name = database_name
        signals.current_city.connect(self.city_city)
        


        if page:
            if cancel_token.is_cancelled():
                return

            if database_type == 1:
                data = []
                for p in page:
                    row = [
                    p["title"],
                    self.city,
                    p["description"],
                    p["state"],
                    self.datetime
                    ]

                    data.append(row)

                signals.ads.emit(data)

                self.__save_sql(page)
                    

            elif database_type == 2:
                data = []
                for p in page:
                    row = [
                    p["title"],
                    self.city,
                    p["description"],
                    p["state"],
                    self.datetime
                    ]

                    data.append(row)

                signals.ads.emit(data)

                self.__save_csv(page)

            else:
                data = []
                for p in page:
                    row = [
                    p["title"],
                    self.city,
                    p["description"],
                    p["state"],
                    self.datetime
                    ]

                    data.append(row)

                signals.ads.emit(data)

                self.__save_sql(page)
                self.__save_csv(page)


            stats.adsfound(len(page))

        level = "good" if state == 200 else "bad"

        log.readed_page(stats.page_count,stats.ads_found)
        signals.page.emit(stats.page_count)
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


    def __save_sql(self,page) -> None:

        try:
            

            if self.database_name != 'test':

                sql_database.create(self.database_name)

            else:

                sql_database.create(':memory:')


            sql_database.create_table()


            for item in page:

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

    def __save_csv(self,page) -> None:
        stats.adssaved(
            save.csv_database(
            self.database_name,
            page
            )
                )
