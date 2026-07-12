import datetime
from storage.json_save_and_load import save_and_load_json
from colorama import Fore,Back,Style,init

init()


json_database = save_and_load_json()


class log_data:
    def __init__(self):
        pass
        

    def search_log(
            self,
            topic,
            city,
            city_ids,
            database_name,
            database_type,
            search_database= None
            ):
        """
        log for search info, what you search
        """

        if search_database == None:
            search_database = 'databases/city_log.json'
        city_log_data = {
                    "topic": topic,
                    "city": city,
                    "city_ids": city_ids,
                    "database_name": database_name,
                    "database_path":f'databases/{database_name}',
                    "database_type":database_type
                }
        

        json_database.save(search_database,city_log_data,type='w')

    def connect_log(
            self,
            conection,
            level,
            url,
            database_name,
            database_path,
            connect_database = None
            ):
        
        """
        log the connecion of a request or session 
        """
        
        if connect_database == None:
        
            connect_database = 'databases/connect_log.json'
        
        connection_data = {
                "datetime":datetime.datetime.now().strftime("%d:%H:%M:%S"),
                "connection":conection,
                "level":level,
                "url":url,
                "database_name":database_name,
                "database_path":database_path
            }
        
        json_database.save(connect_database,connection_data)

    def error_log(
            self,
            error,
            where,
            state,
            error_file = None
            ):
        
        """
        log an error in code
        """


        if error_file == None:
        
            error_database = 'databases/error_log.json'
        
        error_data = {
                "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "state": state,
                "where": where,
                "error_type": type(error).__name__,
                "error": str(error)
            }

        json_database.save(error_file,error_data,type='w')

    def final_log(
            self,
            database_name,
            ads_found,
            ads_saved,
            topic,
            city,
            ads_list_database = None
            ):
        
        """
        log the final report
        """
        
        if ads_list_database == None:
            ads_list_database = 'databases/ads_list_log.json'
        ads_list_data = {
            "datetime":datetime.datetime.now().strftime("%d:%H:%M:%S"),
            "database_name":database_name,
            "topic": topic,
            "city":city,
            "ads_found": ads_found,
            "ads_saved":ads_saved,
        }

        json_database.save(ads_list_database,ads_list_data)

    def readed_page(
            self,
            page,
            ads_in_page,
            readed_page_database = None
            ):
        
        """
        log the readed pages in on session
        """
        
        
        if readed_page_database == None:
            readed_page_database = 'databases/readed_page_log.json'

        readed_page_log = {
            "datetime": datetime.datetime.now().strftime('%d:%H:%M:%S'),
            "page":page,
            "ads_in_page":ads_in_page
        }

        json_database.save(readed_page_database,readed_page_log,type='w')