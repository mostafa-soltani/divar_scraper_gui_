import requests
from unittest.mock import Mock, patch

from core.request_client import RequestClient


def test_post_success():

    client = RequestClient()

    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        "result": "ok"
    }

    with patch.object(
        client.session,
        "post",
        return_value=response
    ):

        data, status = client.post(
            url="http://test.com",
            payloads={},
            headers={}
        )

    assert status == 200
    assert data == {"result": "ok"}


def test_post_invalid_json():

    client = RequestClient()

    response = Mock()
    response.status_code = 200
    response.json.side_effect = ValueError()

    with patch.object(
        client.session,
        "post",
        return_value=response
    ):

        data, status = client.post(
            url="http://test.com",
            payloads={},
            headers={}
        )

    assert data is None
    assert status is None


def test_post_http_error():

    client = RequestClient()

    response = Mock()
    response.status_code = 400

    with patch.object(
        client.session,
        "post",
        return_value=response
    ):

        data, status = client.post(
            url="http://test.com",
            payloads={},
            headers={}
        )

    assert data is None
    assert status is None


def test_post_connection_error():

    client = RequestClient()

    with patch.object(
        client.session,
        "post",
        side_effect=requests.exceptions.ConnectionError()
    ):

        data, status = client.post(
            url="http://test.com",
            payloads={},
            headers={}
        )

    assert data is None
    assert status is None


def test_post_rate_limit_then_success():

    client = RequestClient()

    response_429 = Mock()
    response_429.status_code = 429

    response_200 = Mock()
    response_200.status_code = 200
    response_200.json.return_value = {
        "result": "ok"
    }

    with patch.object(
        client.session,
        "post",
        side_effect=[
            response_429,
            response_200
        ]
    ):

        with patch(
            "time.sleep",
            return_value=None
        ):

            data, status = client.post(
                url="http://test.com",
                payloads={},
                headers={}
            )

    assert status == 200
    assert data == {"result": "ok"}