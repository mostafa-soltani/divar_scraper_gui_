from difflib import get_close_matches
from core.services import json_database


class City_Match:

     def find(self, city_name, cities=None):

        if cities is None:
            cities = json_database.load(
                'databases/city_ids.json'
            )

        if isinstance(cities, dict):
            search_list = cities.keys()

        else:
            search_list = cities

        matches = get_close_matches(
            city_name,
            search_list,
            n=5,
            cutoff=0.3
        )

        return matches if matches else None