# -*- encoding: utf-8 -*-
from unittest.mock import patch


@patch("pyotp.totp.TOTP.provisioning_uri")
@patch("chalicelib.models.DATABASE.save_new_user")
def test_create_new_user(save_new_user_mock, provisioning_uri_mock):
    """ Test if a user can be created as expected """
    from chalicelib.services import create_new_user

    user_id = "johndoe"
    user_secret = "W4L2DMDGQCUGWJRP"
    user_qr_code = f"otpauth://totp/MyApp:johndoe?secret={user_secret}&issuer=MyApp"
    user_qr_code_url = (
        f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={user_qr_code}"
    )

    save_new_user_mock.return_value = {"user_id": user_id, "secret": user_secret}
    provisioning_uri_mock.return_value = user_qr_code

    response = create_new_user(user_id)

    assert response["user"] == user_id
    assert response["qr_code"] == user_qr_code
    assert response["qr_code_url"] == user_qr_code_url


@patch("chalicelib.services.DATABASE.get_user")
@patch("chalicelib.services.TOTP.verify")
def test_verify_user_code(verify_mock, get_user_mock):
    """ Test if code verification works as expected """
    from chalicelib.services import verify_user_code

    user_id = "johndoe"
    user_secret = "W4L2DMDGQCUGWJRP"
    user_code = "123123"

    get_user_mock.return_value = {"user_id": user_id, "secret": user_secret}
    verify_mock.return_value = True

    response = verify_user_code(user_id, user_code)
    assert response == {"code_is_valid": True}

    verify_mock.return_value = False
    response = verify_user_code(user_id, user_code)
    assert response == {"code_is_valid": False}


@patch("chalicelib.models.DATABASE.delete_user")
def test_delete_user(delete_user_mock):
    """ Test if user deletion works as expected """
    from chalicelib.services import delete_user

    user_id = "johndoe"

    delete_user_mock.return_value = True
    assert delete_user(user_id) is True

    delete_user_mock.return_value = False
    assert delete_user(user_id) is False
