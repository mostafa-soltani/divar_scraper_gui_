from filters.use_filter import Use_Filter
from colorama import Fore,Back,Style,init

init()

use_filter = Use_Filter()

POST_ROW = "POST_ROW"

class DivarExtractor:

    def extract(
        self,
        data_json,
        filter_name=None,
        min_price=None,
        max_price=None,
        name_filter=None,
        state_filter=None
    ) -> list:
        """
        extract the ads from raw page and return it

        take data_json,filter_name,min_price,max_price,name_filter,state_filter

        data_json : page in json
        filter_name : to show what filter user want.
        min_price : for price filter , the minimum of price in search.
        max_price : for price filter , the maximum of price in search.
        name_filter : what name or title you want to filter.
        state_filter : what state you want to filter.


        return a dict of ads include title, token, description, addsress,state, url
        """

        extracted_data = []
        try:

            for item in data_json.get("list_widgets", []):

                if item.get("widget_type") != POST_ROW:
                    continue

                post = item.get("data", {})

                # -------------------------
                # apply filter once
                # -------------------------

                if not use_filter.filter_func(
                    post,
                    filter_name,
                    min_price,
                    max_price,
                    name_filter,
                    state_filter):
                    continue

                # -------------------------
                # build output
                # -------------------------

                extracted_data.append({
                    "title": post.get("title"),
                    "address": post.get("bottom_description_text"),
                    "description": post.get("middle_description_text"),
                    "state": post.get("top_description_text"),
                    "token": post.get("token"),
                    "url": f"https://divar.ir/v/{post.get('title')}/{post.get('token')}"
                })

            return extracted_data

        except Exception as e:


            print(Fore.YELLOW+"extract error:", e)

            return []
        

    