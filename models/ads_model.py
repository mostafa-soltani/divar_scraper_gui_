from typing import Any

from PySide6.QtCore import (
    QModelIndex,
    QPersistentModelIndex,
    Qt,
    QAbstractTableModel
)


class AdsModel(QAbstractTableModel):

    def __init__(self,data = None):
        super().__init__()

        self._data = data or []

        self.headers = [
            "title - عنوان",
            "city - شهر",
            "price - قیمت",
            "state - وضعیت",
            "date - تاریخ"
        ]

    def rowCount(self, parent: None):

        return len(self._data)
    
    def columnCount(self, parent: None) -> int:
        return len(self.headers)
    
    def data(self, index, role):

        if role != Qt.DisplayRole:
            return None

        row = index.row()
        column = index.column()

        if row >= len(self._data):
            return None

        if self._data[row] is None:
            return None

        if column >= len(self._data[row]):
            return None

        return str(self._data[row][column])
        

    def headerData(
            self, 
            section, 
            orientation, 
            role) :
        if (
            role == Qt.DisplayRole
            and orientation == Qt.Horizontal
        ):
            return self.headers[section]
        
    def append_rows(self,rows):

        start = len(self._data)
        end = start + len(rows) -1


        self.beginInsertRows(
            QModelIndex(),
            start,
            end
        )

        self._data.extend(rows)

        self.endInsertRows()
        

    
    
