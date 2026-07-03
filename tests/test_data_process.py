from core.request_api import api_request
from config.config import config_api_data,searchconfigs

process = api_request()
ask_data = config_api_data()



data_config = searchconfigs(filter_info=None,
                            filter_name=None,
                            min_price=None,
                            max_price=None,
                            database_name='test',
                            database_type=None)


payloads={
            "city_ids": ["2"],
            "source_view": "SEARCH",
            "disable_recommendation": False,
            "search_data": {
                "query": "ps4"
            }
        }
    


def test_data_processing():
    result = process.request(url = ask_data.url,
                             data_config=data_config,
                             timeout=10,
                             headers=ask_data.headers,
                             payloads=payloads)
    
    assert result == True