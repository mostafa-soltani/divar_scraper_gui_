from extractor.get_city_close_match import City_Match

city_match = City_Match()


def test_city_true():

    city = "ker"

    cities = [
        "kermanshah",
        "kermandareh",
        "horkerman",
        "kerman",
        "shahr kerman"
    ]

    result = city_match.find(city, cities)

    assert result is not None
    assert "kerman" in result


def test_city_false():

    city = "zzz"

    cities = [
        "khoramshahr",
        "mashhad",
        "tehran",
        "london"
    ]

    result = city_match.find(city, cities)

    assert result is None


def test_farsi_city():

    city = "کر"

    cities = [
        "کرمان",
        "کرمانشاه",
        "کردان",
        "تهران",
        "مشهد"
    ]

    result = city_match.find(city, cities)

    assert result is not None
    assert "کرمان" in result