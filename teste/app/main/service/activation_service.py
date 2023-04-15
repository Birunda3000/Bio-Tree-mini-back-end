import random
import string
from time import time

from app.main import db
from app.main.config import Config
from app.main.exceptions import DefaultException
from app.main.model import User

_EXP_ACTIVATION = Config.ACTIVATION_EXP_SECONDS


def token_generate(seed=None, size=64) -> str:

    if seed is not None:
        random.seed(seed)
    return "".join(
        random.SystemRandom().choice(
            string.ascii_uppercase + string.ascii_lowercase + string.digits
        )
        for _ in range(size)
    )


def activate_user(token: str, data: dict[str, str]) -> None:

    user = activation_check_token(token)

    if user.status == "active":
        raise DefaultException("user_already_activated", code=409)

    if user.status == "blocked":
        raise DefaultException("user_is_blocked", code=409)

    new_password = data.get("new_password")
    repeat_new_password = data.get("repeat_new_password")

    if not new_password == repeat_new_password:
        raise DefaultException("passwords_not_match", code=409)

    if not check_pw("", user.password):
        raise DefaultException("password_already_created", code=409)

    user.password = hash_password(new_password)
    user.status = "active"

    db.session.commit()


def activation_check_token(token: str):

    user = User.query.filter_by(activation_token=token).scalar()

    if not user:
        raise DefaultException("token_invalid", code=409)

    if user.activation_token_exp < int(time()):
        raise DefaultException("token_expired", code=401)

    return user


def resend_token(user_id: int) -> None:

    user = User.query.filter_by(id=user_id).scalar()

    if not user:
        raise DefaultException("user_not_found", code=404)

    if user.status == "active":
        raise DefaultException("user_already_activated", code=409)

    if user.status == "blocked":
        raise DefaultException("user_is_blocked", code=409)

    professional = get_professional(professional_id=user.professional_id)

    new_token = token_generate(professional.email)
    user.activation_token = new_token
    user.activation_token_exp = int(time()) + _EXP_ACTIVATION

    db.session.commit()

    send_email_activation(
        to=professional.email, professional_name=professional.name, token=new_token
    )


from app.main.service.email_service import send_email_activation
from app.main.service.password_service import check_pw, hash_password
from app.main.service.professional_service import get_professional
