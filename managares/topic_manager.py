from PySide6.QtWidgets import QMessageBox
from filters.ok_event import KeyFilter

class Topic:
    def __init__(self,widget) -> None:
        self.widget = widget
        self.filter = KeyFilter(self.delete)
        self.widget.topic_to_search.installEventFilter(self.filter)
        pass

    def save(self):

        topic = self.widget.topic.text().strip().lower()

        
        if not topic:
            QMessageBox.warning(self.widget,'warning','the topic section is empty',QMessageBox.StandardButton.Ok)
            return
        
        self.widget.topic_to_search.addItem(topic)
        self.widget.topic.clear()

    def delete(self):
        selected = self.widget.topic_to_search.selectedItems()

        if not selected:
            QMessageBox.warning(self.widget,'warning','nothing selected.',QMessageBox.StandardButton.Ok)
            return
        
        for topic in selected:

            self.widget.topic_to_search.takeItem(
                self.widget.topic_to_search.row(topic)
            )

    def collect(self) -> list:
        topics = []
        for topic_num in range(self.widget.topic_to_search.count()):
            topics.append(self.widget.topic_to_search.item(topic_num).text())
        
        return topics