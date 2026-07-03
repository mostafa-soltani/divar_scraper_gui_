from logs.log import log_data


log = log_data()


def test_log():

    try:

        log.final_log(
            'test.json',
            ads_found='test',
            ads_saved='test',
            topic='test',
            city = 'test',
            ads_list_database='databases/test.json'
        )

        log.connect_log(
            'test',
            level='test',
            url='test',
            database_name='test.json',
            database_path='test',
            connect_database='databases/test.json'
        )
        log.error_log(
            error='test',
            where='test_log.py',
            state='test',
            error_database='databases/test.json'
        )

        log.readed_page(
            page='test',
            ads_in_page='test',
            readed_page_database='databases/test.json'
        )

        log.search_log(
            topic='test',
            city='test',
            city_ids='test',
            database_name='test',
            database_type='test',
            search_database='databases/test.json'
        )

        result = True

    except:
        result = False

    assert result == True