from PySide6.QtWidgets import QMessageBox

class Set_Min_Max:

    def __init__(self,window):
        self.window = window

    def set_price(self) -> tuple:
        minimum = self.window.minimum_price.text().strip()
        maximum = self.window.maximum_price.text().strip()

        if not minimum and not maximum:
            QMessageBox.warning(
                self.window,
                'Price Filter',
                'please Enter at Least One Price'
            )

            return None,None
        

        minimum = int(minimum) if minimum else 0
        maximum = int(maximum) if maximum else 1_000_000_000_000_000

        return minimum,maximum