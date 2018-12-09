from unittest.mock import patch


@patch("chalicelib.utils.datetime")
@patch("builtins.print")
def test_log(print_mock, now_mock):
    from chalicelib.utils import log

    now_datetime = "2010-01-01 00:00:00"
    now_mock.now.return_value = now_datetime

    sender = "me"
    message = "test"
    log(sender, message)

    print_mock.assert_called_with(f"{now_datetime} [{sender}]: {message}")
