from models.ads_model import AdsModel


class TableManager:

    def __init__(self, table):

        self.model = AdsModel([])

        table.setModel(self.model)

    def add_ads(self, data):

        self.model.append_rows(data)