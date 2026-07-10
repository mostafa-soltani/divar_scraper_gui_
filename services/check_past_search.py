import os
from colorama import Fore,Back,Style,init
from core.services import json_database,log




class Check_Past_search:
    def __init__(self):
        
        self.city_log_database = 'databases/city_log.json'

    def Past_Search(
            self
            ):

        """
        past search is is user want to continue the last search or want a new search
        """

        if not os.path.exists(self.city_log_database) or os.path.getsize(self.city_log_database) == 0:
            return None
        else:

            data = json_database.load(self.city_log_database)

            topic,city,city_ids,database_name,path,database_type = data.values()

            return topic,city,city_ids,database_name,database_type
    
    