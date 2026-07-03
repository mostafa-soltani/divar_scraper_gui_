from deep_translator import (GoogleTranslator)


class Translate:

    def transtale_data(self,data) -> str:
        return GoogleTranslator(source='auto',target='en').translate(data)