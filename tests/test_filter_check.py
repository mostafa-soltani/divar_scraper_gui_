from filters.filter_check import Ask_filter


def test_no_filter(monkeypatch):

    monkeypatch.setattr(
        "builtins.input",
        lambda *args: "no"
    )

    ask = Ask_filter()

    result = ask.check_filter()

    assert result == (
        None,
        None,
        0,
        1000000000000000
    )


def test_name_filter(monkeypatch):

    inputs = iter([
        "yes",
        "name",
        "ps4"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda *args: next(inputs)
    )

    ask = Ask_filter()

    result = ask.check_filter()

    assert result == (
        "name_filter",
        "ps4",
        0,  
        1000000000000000
    )


def test_state_filter(monkeypatch):

    inputs = iter([
        "yes",
        "state",
        "new"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda *args: next(inputs)
    )

    ask = Ask_filter()

    result = ask.check_filter()

    assert result == (
        "state_filter",
        "new",
        0,
        1000000000000000
    )


def test_price_filter(monkeypatch):

    inputs = iter([
        "yes",
        "price",
        "1000000",
        "5000000"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda *args: next(inputs)
    )

    ask = Ask_filter()

    result = ask.check_filter()

    assert result == (
        "price_filter",
        None,
        "1000000",
        "5000000"
    )

def test_persian_name_filter(monkeypatch):

    inputs = iter([
        "yes",
        "اسم",
        "iphone"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda *args: next(inputs)
    )

    ask = Ask_filter()

    result = ask.check_filter()

    assert result[0] == "name_filter"


def test_persian_price_filter(monkeypatch):

    inputs = iter([
        "yes",
        "قیمت",
        "100",
        "1000"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda *args: next(inputs)
    )

    ask = Ask_filter()

    result = ask.check_filter()

    assert result[0] == "price_filter"