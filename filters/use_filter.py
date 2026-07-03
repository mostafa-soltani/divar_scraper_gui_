from filters.filter import FilterAds


filter_ads = FilterAds()

class Use_Filter:

    def filter_func(
            self,
            post,
            filter_name,
            min_price,
            max_price,
            name_filter,
            state_filter

        ) -> bool:

        """
        return True or False for filter you choose
        """


        NAME_FILTER = [
        'name_filter',
        'name',
        'name filter',
        'اسم'
        ]

        STATE_FILTER = [
                'state',
                'state_filter',
                'state filter',
                'state-filter',
                'وضعیت'
            ]

        PRICE_STATE = [
                'price filter',
                'price',
                'price filter',
                'قیمت'
            ]

        if filter_name in PRICE_STATE:

            return filter_ads.price_filter(
                post.get("middle_description_text"),
                min_price= min_price,
                max_price= max_price
            )

        elif filter_name in NAME_FILTER:

            return filter_ads.name_filter(
                post.get("title"),
                name_filter
            )

        elif filter_name in STATE_FILTER:

            return filter_ads.state_filter(
                post.get("top_description_text"),
                state_filter
            )

        else:

            return True
