from storage.city_resolver import CityResolver


resolver = CityResolver()


def test_city_resolver():

    cities = resolver.get_city_ids('kho')

    if cities:
        result = True
    else:
        result = False

    assert result == True