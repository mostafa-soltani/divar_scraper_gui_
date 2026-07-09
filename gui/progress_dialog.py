from PySide6.QtWidgets import QMessageBox


class Progress:

    def __init__(self, window, worker):
        self.window = window
        self.worker = worker

    def search_finished(self):
        QMessageBox.information(
            self.window,
            "Done",
            "Search completed."
        )

    def search_cancelled(self):
        QMessageBox.information(
            self.window,
            "Cancelled",
            "Search cancelled."
        )

    def show_error(self,message):
        QMessageBox.warning(
            self.window,
            'warning',
            message
        )
        return
    
    
    def setup(self):
        self.worker.signals.progress.connect(
            self.window.progressBar.setValue
        )

        self.worker.signals.finished.connect(
            self._progress_finished
        )

        self.worker.signals.error.connect(
            self._show_error
        )

        self.worker.signals.current_topic.connect(
            self.__update_topic
        )

        self.worker.signals.current_city.connect(
            self.__update_city
        )

        self.worker.signals.current_database.connect(
            self.__update_database
        )

    def _progress_finished(self):
        QMessageBox.information(
            self.window,
            "Search Done",
            "Search completed successfully."
        )

    def _show_error(self, message):
        QMessageBox.critical(
            self.window,
            "Error",
            message
        )

    def __update_topic(self, topic):
        print(topic)
        self.window.current_topic.setText(topic)

    def __update_city(self, city):
        print(city)
        self.window.current_city.setText(city)

    def __update_database(self, database):
        print(database)
        self.window.current_db_name.setText(database)