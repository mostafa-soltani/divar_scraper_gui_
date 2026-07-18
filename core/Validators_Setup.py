from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtCore import QRegularExpression


class Validator_price:
    def __init__(self,widget) -> None:
        self.widget = widget


    def setup(self):
        validator = QRegularExpressionValidator(
            QRegularExpression(r"\d{1,15}")
        )


        for item in (
            self.widget.minimum_price,
            self.widget.maximum_price
        ):
            item.setValidator(validator)