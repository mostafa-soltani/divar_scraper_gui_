class Log_manager:
    def __init__(self,widget,log_signal):
        self.widget = widget
        self.logsignal = log_signal


    def connect_open_app(self):
        item = 'open the app'
        self.widget.logs.addItem(item)

    def connect_past_search(self):
        item = 'using last search'
        self.widget.logs.addItem(item)

    def connect_topics(self,message):
        message = f'topics {message}'
        self.widget.logs.addItem(message)
    
    def connect_cities(self,message):
        message = f'cities {message.keys()}'
        self.widget.logs.addItem(message)

    def connect_db_name(self,message):
        message = f'databases {message}'
        self.widget.logs.addItem(message)

    def connect_db_type(self,message):
        message = f'databases type {message}'
        self.widget.logs.addItem(message)

    def connect_start_search(self):
        item = 'starting searching'
        self.widget.logs.addItem(item)

    def connect_connection(self,message):
        self.widget.logs.addItem(message)

    def connect_time(self,date):
        self.widget.logs.addItem(date)
        



    def show_log(self):

        self.logsignal.open_app.connect(self.connect_open_app)

        self.logsignal.past_search.connect(self.connect_past_search)

        self.logsignal.topics.connect(self.connect_topics)

        self.logsignal.cities.connect(self.connect_cities)

        self.logsignal.databases.connect(self.connect_db_name)

        self.logsignal.database_type.connect(self.connect_db_type)

        self.logsignal.start_search.connect(self.connect_start_search)

        self.logsignal.connection.connect(self.connect_connection)

        self.logsignal.date_time.connect(self.connect_time)