from PySide6.QtWidgets import QMessageBox
from storage.city_resolver import CityResolver
from filters.ok_event import KeyFilter


find_city = CityResolver()

class City:
    def __init__(self,widgets,config) -> None:
        self.widgets = widgets
        self.loaded_cities = set()
        self.selected_cities = config.selected_cities
        self.filter = KeyFilter(self.delete)
        self.widgets.added_cities.installEventFilter(self.filter)

    
    def _city_search(self, city):
        new_cities = find_city.get_city_ids(city)


        if not new_cities:
            QMessageBox.warning(
                self.widgets,
                "Warning",
                "The city section is empty.",
                QMessageBox.StandardButton.Ok,
            )
            return
        
        for city_name, city_id in new_cities.items():
            if city_name not in self.loaded_cities:
                self.loaded_cities.add(city_name)
                self.widgets.founded_cities.addItem(city_name)

            elif city_name in self.selected_cities.keys():

                self.selected_cities.update(new_cities)

            self.selected_cities[city_name] = city_id

        return self.selected_cities



    def save(self):
        city = self.widgets.city.text().strip().lower()

        if not city:
            QMessageBox.warning(self.widgets,'warning','the city section is empty',QMessageBox.StandardButton.Ok)

        self._city_search(city)
        self.widgets.city.clear()



    def delete(self):
        selected = self.widgets.added_cities.selectedItems()

        if not selected:
            QMessageBox.warning(self.widgets,'warning','nothing selected.',QMessageBox.StandardButton.Ok)
            return
        
        for city in selected:

            self.widgets.added_cities.takeItem(
                self.widgets.added_cities.row(city)
            )

    def collect(self):
        cities = {}
        for city_num in range(self.widgets.added_cities.count()):
            city = self.widgets.added_cities.item(city_num).text()
            cities[city] = self.selected_cities[city]

        return cities

    def unchoose_city(self):
        selected = self.widgets.added_cities.selectedItems()

        if not selected:
            QMessageBox.warning(
                self.widgets,
                'warning',
                'nothing selected.',
                QMessageBox.StandardButton.Ok
            )
            return
        
        for i in selected:
            self.widgets.founded_cities.addItem(i)
            self.widgets.added_cities.takeItem(i)