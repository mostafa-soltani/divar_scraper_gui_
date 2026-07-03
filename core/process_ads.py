import os
from core.services import stats,log,save,extractor
from storage.SQLite_database import SQLDatabase
from config.ad import Ad

sql_database = SQLDatabase()

ad_ = Ad

class process_ads:
    """
    process ads is a class to process pages of data and ads and save the ads in databases who the user choose 
    """

    def __init__(self):
        pass

    def process(
            self,
            data_config,
            page_json,
            state,
            url
            ) -> object:
        """
        process ads is a class to process pages of data and ads and save the ads in databases who the user choose.

        take data config, page_json,state,url

        data_config : all of data that needed for process inclode filter informations.
        page_json : the page that readed from site with connction.
        state : the status code from site for save in databases.
        url : for save in log.
        """
        page = extractor.extract(
            data_json=page_json,
            filter_name=data_config.filter_name,
            min_price=data_config.min_price,
            max_price=data_config.max_price,
            name_filter=data_config.filter_value,
            state_filter=data_config.filter_value
        )

        stats.pagecount()
        self.database_name = data_config.database_name


        if page:

            if data_config.database_type == 1:

                self.__save_sql(page)
                

            elif data_config.database_type == 2:
                self.__save_csv(page)

            else:
                self.__save_sql(page)
                self.__save_csv(page)


            stats.adsfound(len(page))

        level = "good" if state == 200 else "bad"

        log.readed_page(stats.page_count,stats.ads_found)

        log.connect_log(
                    conection=state,
                    level=level,
                    url=url,
                    database_name='databases/connect_log.json',
                    database_path=os.path.abspath('databases/connect_log.json')
                    )
        
        return sql_database

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
