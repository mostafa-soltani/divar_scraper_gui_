

class save_data:

    def __init__(self):
        self.topic = None
        self.city = None
        self.database_name = None
        self.database_type = None
        self.filter_name = None
        self.filter_value = None
        self.min_price = 0
        self.max_price = 0
        self.city_id = None

    def Save(self,topic,city,database_name,database_type,minimum_price,maximum_price,filter_name,filter_value,city_id = None):
        self.topic = topic
        self.city = city
        self.database_name = database_name
        self.database_type = database_type
        self.filter_name = filter_name
        self.filter_value = filter_value
        self.minimum = minimum_price
        self.maximum = maximum_price
        self.city_id = city_id
        