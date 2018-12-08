# -*- encoding: utf-8 -*-
""" Test Services """

import re

from unittest.mock import patch


@patch("boto3.resource")
def test_create_new_user(boto_mock):
    """ Test if a user can be created as expected """
    from chalicelib.services import create_new_user

    user_id = "johndoe@something.com"
    res = create_new_user(user_id)

    assert res["user"] == user_id
    assert (
        re.search(
            r"otpauth://totp/MyApp:johndoe%40something.com\?secret=(.+)"
            r"&issuer=MyApp",
            res["qr_code"],
        )
        is not None
    )
    assert (
        re.search(
            r"https://api.qrserver.com/v1/create-qr-code/\?size=150x150&"
            r"data=otpauth://totp/MyApp:johndoe%40something.com\?secret=(.+)"
            r"&issuer=MyApp",
            res["qr_code_url"],
        )
        is not None
    )


@patch("chalicelib.services.DATABASE.get_user")
@patch("chalicelib.services.TOTP.verify")
def test_verify_user_code(verify_mock, boto_mock):
    """ Test if code verification works as expected """
    from chalicelib.services import verify_user_code

    mock_val = dict(user_id="johndoe@something.com", secret="J6EBMHHXTCCCZ5RC")
    boto_mock.return_value = mock_val
    verify_mock.return_value = True

    user_id = "johndoe@something.com"
    code = "code_returned_by_app"

    res = verify_user_code(user_id, code)
    assert res is True

    verify_mock.return_value = False
    res = verify_user_code(user_id, code)
    assert res is False
