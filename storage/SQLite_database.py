import sqlite3
from core.services import stats
import os



class SQLDatabase:
    """
    save data in SQLite 
    use like this :
    db = SQLDatabase()


    db.create('database_name')


    db.create_table()


    db.insert(data) 
    if data is one line else 


    
    for line in data:
        db.insert(line)

    #db.close()


    and if you want to search in titel just:

    db.search(title_user)
        
    """

    def __init__(self):
        self.connection = None
        self.i = 1

    def create(self, database_name) -> object:
        """
        create a connection to sql database
        """


        folder = os.path.dirname(database_name)

        if folder and not os.path.exists(folder):
            os.makedirs(folder)

        if database_name == ":memory:":
            self.connection = sqlite3.connect(":memory:")

        elif database_name.endswith(".db"):
            self.connection = sqlite3.connect(database_name)

        else:
            self.connection = sqlite3.connect(
                f"databases/{database_name}.db"
            )

        return self

    def create_table(self) -> None:
        """
        create table in database you give 
        table ads with 
        id, token,title,address,description,state,url
        """

        cur = self.connection.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS ads(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token TEXT UNIQUE,
            title TEXT ,
            address TEXT ,
            description TEXT ,
            state TEXT ,
            url TEXT
        )
        """)

        '''cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_title
        ON ads(title)
        """)

        cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_state
        ON ads(state)
        """)

        cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_address
        ON ads(address)
        """)'''

        self.connection.commit()

    def exists(self, token) -> bool:
        """
        check if a token already exist or not
        """

        cur = self.connection.cursor()

        cur.execute(
            "SELECT token FROM ads WHERE token = ?",
            (token,)
        )

        result = cur.fetchone()


        return result is not None

    def insert(self,ad_confog):
        """
        insert data in table ads in your database
        """

        cur = self.connection.cursor()

        cur.execute(
            """
            INSERT OR IGNORE INTO ads(
                token,
                title,
                address,
                description,
                state,
                url
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                ad_confog.token,
                ad_confog.title,
                ad_confog.address,
                ad_confog.description,
                ad_confog.state,
                ad_confog.url
            )
        )
        stats.ads_saved += 1

        self.connection.commit()

    def close(self):
        """
        close the connection
        """

        if self.connection:

            self.connection.commit()

            self.connection.close()

    def search(self,word) -> list:
        """
        search in title for what you want
        """

        coursor = self.connection.cursor()

        coursor.execute("""
            SELECT *
            FROM ads
            WHERE title LIKE ?            
            """,
            (F"%{word}%"))
        

        return coursor.fetchall()
    

