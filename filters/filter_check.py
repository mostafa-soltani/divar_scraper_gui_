from colorama import Fore,Back,Style,init


class Ask_filter:

    def check_filter(self) :

        """
        check filter is a function for check user wants what filter for its data to save by

        return filter_name, filter_info, min_price, max_price
        """

        filter_info = None
        filter_name = None
        min_price = 0
        max_price = 1000000000000000
        print(Fore.YELLOW+'do you want to filter data before saving? [yes or no]')
        answer = str(input(Fore.BLUE))

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

        if answer == "yes":

            print(Fore.YELLOW+"which filter? [name/state/price]")
            filter_ = input(Fore.BLUE)

            if filter_ in NAME_FILTER:

                filter_name = "name_filter"
                filter_info = input("name: ")

                return filter_name, filter_info, min_price, max_price

            elif filter_ in STATE_FILTER:

                filter_name = "state_filter"
                filter_info = input("state: ")

                return filter_name, filter_info, min_price, max_price

            elif filter_ in PRICE_STATE:

                filter_name = "price_filter"

                min_price = input("min: ")
                max_price = input("max: ")

                return filter_name, None, min_price, max_price

        else:

            return None, None, min_price, max_price