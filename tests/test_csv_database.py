from storage.csv_database import csv_database
import os


csv_test = csv_database()

def test_csv():

    data = [{"title":"test",
            "address":"test",
            "description":'test',
            "state":"test",
            "token":'test',
            "url":"test"}]
    if os.path.exists("databases/test.csv"):
        os.remove("databases/test.csv")
    
    saved = csv_test.csv_database('test',data)

    if saved:
        result = True

    else:
        result = False

    assert result == True