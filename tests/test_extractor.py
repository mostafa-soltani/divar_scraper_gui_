from core.HTTP_CLIENT import Paginator
from core.request_client import RequestClient
from config.config import config_api_data
from extractor.extract_data import DivarExtractor
import json,os

client = RequestClient()
ask_data = config_api_data()
extrctor = DivarExtractor()

def test_extractor():

    test_file = "databases/test_page.json"

    payloads = {
            "city_ids": ["2"],
            "source_view": "SEARCH",
            "disable_recommendation": False,
            "search_data": {
                "query": 'ps4'
            }
        }


    if not os.path.exists(test_file):

        paginator = Paginator(
            client=client,
            url=ask_data.url,
            headers=ask_data.headers,
            payloads=payloads,
            timeout=2
        )


        saved = False

        for page_json, _ in paginator:

            saved = True

            with open(
                test_file,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    page_json,
                    f,
                    ensure_ascii=False,
                    indent=4
                )

            break


        assert saved == True



    with open(
        test_file,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)



    ads = extrctor.extract(
        data_json=data
    )


    assert ads is not None

    assert len(ads) > 0