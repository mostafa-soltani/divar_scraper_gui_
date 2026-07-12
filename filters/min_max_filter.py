from PySide6.QtWidgets import QMessageBox

class Set_Min_Max:

    def __init__(self,window):
        self.widget = window

    def set_price(self) -> tuple:
        minimum = self.widget.minimum_price.text().strip()
        maximum = self.widget.maximum_price.text().strip()

        if not minimum and not maximum:
            QMessageBox.warning(
                self.widget,
                'Price Filter',
                'please Enter at Least One Price'
            )

            return None,None
        

        minimum = int(minimum) if minimum else 0
        maximum = int(maximum) if maximum else 1_000_000_000_000_000

        return minimum,maximum