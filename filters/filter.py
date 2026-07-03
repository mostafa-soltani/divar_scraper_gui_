import re


class FilterAds:

    FA_TO_EN = str.maketrans(
        "۰۱۲۳۴۵۶۷۸۹",
        "0123456789"
    )

    @staticmethod
    def extract_price(price_text):
        """
        return a int number for price in description and replace persian num for english
        """

        if not price_text:
            return None

        digits = re.sub(
            r"[^0-9۰-۹]",
            "",
            price_text
        )

        if not digits:
            return None

        digits = digits.translate(
            FilterAds.FA_TO_EN
        )

        return int(digits)

    @staticmethod
    def price_filter(price_text, min_price=None, max_price=None) -> bool:
        """
        return a check for price filter if the price is between to min and max
        """

        price = FilterAds.extract_price(price_text)

        if price is None:
            return False

        if min_price is not None:
            min_price = int(
                str(min_price).replace(",", "")
            )

        if max_price is not None:
            max_price = int(
                str(max_price).replace(",", "")
            )

        if min_price is not None and price < min_price:
            return False

        if max_price is not None and price > max_price:
            return False

        return True


    def name_filter(self, text, search)-> bool:

        """
        return the name you want to filter
        """

        if not text or not search:
            return False

        text = str(text).strip().lower()
        search = str(search).strip().lower()

        return search in text


    def state_filter(self, state, asked) -> bool:

        """
        return is the state you want is there or not
        """

        if not state or not asked:
            return False

        state = str(state).strip().lower()
        asked = str(asked).strip().lower()

        return asked in state
