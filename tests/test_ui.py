from ui.check_past_search import Check_Past_search

ui = Check_Past_search()


def test_ui():

    topic,city,city_ids,database_name,database_type = ui.Past_Search(status_search='yes')

    assert topic is not None
    assert city is not None
    assert city_ids is not None
    assert database_name is not None
    assert database_type is not None