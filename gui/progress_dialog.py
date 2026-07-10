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
        try:
            self.worker.signals.progress.connect(
                self.window.progressBar.setValue
            )
        except Exception as e:
            print(e)


        try:
            print('update topic')
            self.worker.signals.current_topic.connect(
                self.__update_topic
                

            )
        except Exception as e:
            print(e)

        try:
        
            print('update city')

            self.worker.signals.current_city.connect(
                self.__update_city

            )
        except Exception as e:
            print(e)
        try:
            print('update db')
            self.worker.signals.current_database.connect(
                
                self.__update_database
            )
        except Exception as e:
            print(e)


        self.worker.signals.finished.connect(
            self._progress_finished
        )

        self.worker.signals.error.connect(
            self._show_error
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
        print("TOPIC RECEIVED")
        self.window.current_topic.setText(topic)

    def __update_city(self, city):
        print("CITY RECEIVED")
        self.window.current_city.setText(city)

    def __update_database(self, database):
        print("DATABASE RECEIVED")
        self.window.current_db_name.setText(database)