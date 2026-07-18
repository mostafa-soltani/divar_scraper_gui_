from filters.min_max_filter import Set_Min_Max


class Filter_Manager:

    def __init__(self,widget):
        self.widget = widget
        self.set_min_max = Set_Min_Max(self.widget)


    def get_price(self):

        self.minimum,self.maximum = self.set_min_max.set_price()
        return self.minimum,self.maximum

    def get_name(self):
        self.name_value = self.widget.name_str.text().strip().lower()
        return self.name_value

    def get_state(self):

        self.state_value = self.widget.state_str.text().strip().lower()

        return self.state_value
