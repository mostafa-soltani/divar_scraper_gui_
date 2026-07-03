from filters.filter import FilterAds


def test_extract_price_persian():

    result = FilterAds.extract_price(
        "۵۳,۰۰۰,۰۰۰ تومان"
    )

    assert result == 53000000


def test_extract_price_english():

    result = FilterAds.extract_price(
        "12,500,000"
    )

    assert result == 12500000


def test_extract_price_none():

    result = FilterAds.extract_price(None)

    assert result is None


def test_extract_price_no_digits():

    result = FilterAds.extract_price(
        "توافقی"
    )

    assert result is None


def test_price_filter_in_range():

    result = FilterAds.price_filter(
        "۵۰,۰۰۰,۰۰۰ تومان",
        min_price=40000000,
        max_price=60000000
    )

    assert result is True


def test_price_filter_less_than_min():

    result = FilterAds.price_filter(
        "۲۰,۰۰۰,۰۰۰ تومان",
        min_price=30000000,
        max_price=60000000
    )

    assert result is False


def test_price_filter_greater_than_max():

    result = FilterAds.price_filter(
        "۸۰,۰۰۰,۰۰۰ تومان",
        min_price=30000000,
        max_price=60000000
    )

    assert result is False


def test_price_filter_invalid_price():

    result = FilterAds.price_filter(
        "توافقی",
        min_price=1,
        max_price=100
    )

    assert result is False


def test_name_filter_true():

    f = FilterAds()

    result = f.name_filter(
        "PlayStation 4 Slim",
        "playstation"
    )

    assert result is True


def test_name_filter_false():

    f = FilterAds()

    result = f.name_filter(
        "Xbox Series X",
        "ps4"
    )

    assert result is False


def test_name_filter_empty():

    f = FilterAds()

    result = f.name_filter(
        "",
        "ps4"
    )

    assert result is False


def test_state_filter_true():

    f = FilterAds()

    result = f.state_filter(
        "در حد نو",
        "نو"
    )

    assert result is True


def test_state_filter_false():

    f = FilterAds()

    result = f.state_filter(
        "کارکرده",
        "نو"
    )

    assert result is False


def test_state_filter_empty():

    f = FilterAds()

    result = f.state_filter(
        None,
        "نو"
    )

    assert result is False

def test_price_filter_only_min():

    assert FilterAds.price_filter(
        "۵۰,۰۰۰,۰۰۰ تومان",
        min_price=40000000
    ) is True


def test_price_filter_only_max():

    assert FilterAds.price_filter(
        "۵۰,۰۰۰,۰۰۰ تومان",
        max_price=60000000
    ) is True