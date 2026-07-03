from storage.SQLite_database import SQLDatabase
from core.services import log
from config.ad import Ad


def test_SQLite():

    db = SQLDatabase()

    db.create(':memory:')
    db.create_table()

    ad = Ad(
        title='test title',
        address='test address',
        description='test',
        state='test',
        token='test_token',
        url='test'
    )

    db.insert(ad)

    result = db.exists(ad.token)

    assert result is True

    db.close()


def test_duplicate_token():

    db = SQLDatabase()

    db.create(':memory:')
    db.create_table()

    ad = Ad(
        title='test',
        address='test',
        description='test',
        state='test',
        token='same_token',
        url='test'
    )

    db.insert(ad)
    db.insert(ad)

    # بررسی تعداد رکوردها



def test_not_exists():

    db = SQLDatabase()

    db.create(':memory:')
    db.create_table()

    assert db.exists("unknown_token") is False

    db.close()

def test_create_table_twice():

    db = SQLDatabase()

    db.create(':memory:')

    db.create_table()
    db.create_table()

    db.close()