import requests
from colorama import Fore,Back,Style,init
from core.services import json_database,translate
import os


init()

class CityResolver:

    def __init__(self):
        self.url = "https://api.divar.ir/v8/fields-search"
        self.headers = {
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/json"
        }

    def get_city_ids(self, city_name) -> dict:

        """
        search by the city user give and find city_ids related to that city and save on json file and return

        take city_name

        city_name : the city user give.

        return dict of city and city_ids
        """

        cities = {}
        print(Fore.YELLOW+"city_name =", city_name)

        if not city_name:
            print(Fore.YELLOW+'city not in search: [default = teharn]')
            return {
                "city": "تهران",
                "city_id": "1"
            }

        payload = {
            "field": "cities",
            "q": city_name,
            "source": "filter"
        }

        r = requests.post(
            url=self.url,
            json=payload,
            headers=self.headers
        )

        city_list = r.json()

        results = city_list.get("results", [])

        if not results:
            print(Fore.YELLOW+'city not in search: [default = teharn]')
            return {
                "city": "تهران",
                "city_id": "1"
            }

        for city in results:
            cities[translate.transtale_data(city['enumName']).lower()] = city['enum']
            print(cities)

        if os.path.getsize('databases/city_ids.json') != 0:
            data = json_database.load('databases/city_ids.json')

            for city in cities:
                if city not in data:
                    print(city, "duplicate")
                    data.update(cities)
            
        else:
            
            json_database.save('databases/city_ids.json',cities)
      
        return cities
    

