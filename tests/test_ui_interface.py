from unittest.mock import patch
from ui.user_interface import user_interface


def test_user_input_with_city_file():

    ui = user_interface()

    with patch("builtins.input") as mock_input:

        mock_input.side_effect = [
            "ps4",
            "ker",
            "mydb",
            "1"
        ]

        with patch("os.path.exists", return_value=True):

            with patch("os.path.getsize", return_value=100):

                with patch.object(
                    ui,
                    "_user_interface__read_file",
                    return_value=("kerman", "2")
                ):

                    result = ui.User_Input()

    assert result == (
        "ps4",
        "kerman",
        "2",
        "mydb",
        1
    )

from unittest.mock import patch
from ui.user_interface import user_interface

def test_user_input_without_city_file():

    ui = user_interface()

    with patch("builtins.input") as mock_input:

        mock_input.side_effect = [
            "ps4",
            "ker",
            "mydb",
            "1"
        ]

        with patch("os.path.exists", return_value=False):

            with patch.object(
                ui,
                "_user_interface__search_city",
                return_value=("kerman", "2")
            ):

                result = ui.User_Input()

    assert result == (
        "ps4",
        "kerman",
        "2",
        "mydb",
        1
    )



from unittest.mock import patch
from ui.user_interface import user_interface


def test_database_default_name():

    ui = user_interface()

    with patch("builtins.input") as mock_input:

        mock_input.side_effect = [
            "ps4",
            "ker",
            "",
            "1"
        ]

        with patch("os.path.exists", return_value=True):

            with patch("os.path.getsize", return_value=100):

                with patch.object(
                    ui,
                    "_user_interface__read_file",
                    return_value=("kerman", "2")
                ):

                    result = ui.User_Input()

    assert result[3] is not None

from unittest.mock import patch
from ui.user_interface import user_interface


def test_read_file_exception():

    ui = user_interface()

    with patch("os.path.getsize", side_effect=Exception("error")):

        city, city_id = ui._user_interface__read_file("ker")

    assert city == "tehran"
    assert city_id == "1"