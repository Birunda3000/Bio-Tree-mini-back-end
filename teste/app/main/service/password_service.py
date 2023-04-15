from time import time

from app.main import db
from app.main.config import Config
from app.main.exceptions import DefaultException
from app.main.model import Professional, User

_EXP_ACTIVATION = Config.ACTIVATION_EXP_SECONDS


def change_password(data: dict[str, str], user_id: int) -> None:

    user = get_user(user_id=user_id)

    current_password = data.get("current_password")
    new_password = data.get("new_password")
    repeat_new_password = data.get("repeat_new_password")

    if not new_password == repeat_new_password:
        raise DefaultException("passwords_not_match", code=409)

    if not check_pw(current_password, user.password):
        raise DefaultException("password_incorrect_information", code=409)

    user.password = hash_password(new_password)

    db.session.commit()


def forgot_password(data: dict[str, str]) -> None:

    professional = Professional.query.filter_by(email=data.get("email")).scalar()

    if not professional:
        raise DefaultException("professional_not_found", code=404)

    user = User.query.filter_by(professional_id=professional.id).scalar()

    if not user:
        raise DefaultException("user_not_found", code=404)

    if user.status != "active":
        raise DefaultException("user_not_actived", code=409)

    token = token_generate(professional.email)
    user.reset_password_token = token
    user.reset_password_token_exp = int(time()) + _EXP_ACTIVATION

    db.session.commit()

    send_email_recovery(
        to=professional.email, professional_name=professional.name, token=token
    )


def password_check_token(token: str):

    user = User.query.filter_by(reset_password_token=token).scalar()

    if not user:
        raise DefaultException("token_invalid", code=409)

    if user.reset_password_token_exp < int(time()):
        raise DefaultException("token_expired", code=401)

    return user


def redefine_password(data: dict[str, str], token: str) -> None:

    user = password_check_token(token)

    if user.status != "active":
        raise DefaultException("user_not_active", code=409)

    if user.reset_password_token_exp < int(time()):
        raise DefaultException("token_expired", code=401)

    new_password = data.get("new_password")
    repeat_new_password = data.get("repeat_new_password")

    if not new_password == repeat_new_password:
        raise DefaultException("passwords_not_match", code=409)

    user.password = hash_password(new_password)

    db.session.commit()


from app.main.service.activation_service import token_generate
from app.main.service.auth_service import check_pw, hash_password
from app.main.service.email_service import send_email_recovery
from app.main.service.user_service import get_user
