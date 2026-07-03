import csv
import os

class csv_database:

    def __init__(self):
        self.database_name = None

    def csv_database(self, database_name, ads) -> int:

        """
        csv database is for saving data's in csv file in databases/ path.

        take database_name, ads

        database_name : name of database you want to save.
        ads : data's that is saved

        return a int that is the number of ads is saved.
        """

        check = set()
        saved = 0
        if database_name.endswith('.csv') and database_name.starstwith('databases/'):
            pass
        else:
            database_name = f'databases/{database_name}.csv'
        
        self.database_name = database_name

        
        
        file_exists = os.path.exists(self.database_name)

        

        if file_exists:

            with open(self.database_name, "r", encoding="utf-8-sig") as handle:

                reader = csv.reader(handle)

                next(reader, None)

                for row in reader:

                    if len(row) >= 6:
                        check.add(row[4].strip())

        with open(self.database_name, "a", newline="", encoding="utf-8-sig") as handle:
            
            writer = csv.writer(handle)

            if not file_exists or os.path.getsize(self.database_name) == 0:

                writer.writerow([
                    "title",
                    "address",
                    "description",
                    "state",
                    "token",
                    "url"
                ])

            for item in ads:


                token = item.get("token")

                if token in check:
                    continue

                check.add(token)

                writer.writerow([
                    item.get("title"),
                    item.get("address"),
                    item.get("description"),
                    item.get("state"),
                    token,
                    item.get("url")
                ])

                saved += 1

            return saved
        
