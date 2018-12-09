from pyotp.totp import TOTP

from chalicelib.models import DATABASE
from chalicelib.config import APP_NAME


def create_new_user(user_id):

    user = DATABASE.save_new_user(user_id)

    qr_code = TOTP(user["secret"]).provisioning_uri(
        user["user_id"], issuer_name=APP_NAME
    )

    qr_code_url = (
        f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={qr_code}"
    )

    return {"user": user["user_id"], "qr_code": qr_code, "qr_code_url": qr_code_url}


def verify_user_code(user_id, code):
    user = DATABASE.get_user(user_id)
    return {"code_is_valid": TOTP(user["secret"]).verify(code)}


def delete_user(user_id):
    return DATABASE.delete_user(user_id)
