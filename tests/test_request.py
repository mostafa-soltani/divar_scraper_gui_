from core.request_api import api_request
from core.HTTP_CLIENT import Paginator
from core.request_client import RequestClient
from config.config import config_api_data

request = api_request()
ask_data = config_api_data()
client = RequestClient()


def test_request():

    paginator = Paginator(
        client=client,
        url=ask_data.url,
        headers=ask_data.headers,
        payloads={
            "city_ids": ["2"],
            "source_view": "SEARCH",
            "disable_recommendation": False,
            "search_data": {
                "query": "ps4"
            }
        },
        timeout=10
    )


    received = False


    for page_json, status in paginator:

        if status == 200 and page_json:

            received = True

            break


    assert received == True