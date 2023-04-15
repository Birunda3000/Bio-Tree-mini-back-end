from math import ceil
from time import time

from werkzeug.datastructures import ImmutableMultiDict

from app.main import db
from app.main.config import Config
from app.main.exceptions import DefaultException
from app.main.model import User

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE
_EXP_ACTIVATION = Config.ACTIVATION_EXP_SECONDS


def get_users(params: ImmutableMultiDict):

    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)
    login = params.get("login", type=str)

    filters = []

    if login:
        filters.append(User.login.ilike(f"%{login}%"))

    pagination = (
        User.query.filter(*filters)
        .order_by(User.id)
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return {
        "current_page": page,
        "total_items": pagination.total,
        "total_pages": ceil(pagination.total / per_page),
        "items": pagination.items,
    }


def get_user_by_id(user_id: int) -> None:
    return get_user(user_id=user_id, active_check=False)


def save_new_user(data: dict[str, str]) -> None:

    user = User.query.filter_by(login=data.get("login")).scalar()

    if user:
        raise DefaultException("username_in_use", code=409)

    professional = get_professional(professional_id=data.get("professional_id"))

    pswd = hash_password("")

    new_user = User(
        professional_id=data.get("professional_id"),
        login=data.get("login"),
        password=pswd,
        activation_token=token_generate(professional.email),
        activation_token_exp=int(time()) + _EXP_ACTIVATION,
        reset_password_token=None,
        reset_password_token_exp=None,
    )

    db.session.add(new_user)
    db.session.commit()

    send_email_activation(
        to=professional.email,
        professional_name=professional.name,
        token=new_user.activation_token,
    )


def update_user(user_id: int, data: dict[str, any]) -> None:

    user = get_user(user_id=user_id, active_check=False, blocked_check=False)

    if user.status == "waitActivation":
        raise DefaultException("user_never_activated", code=409)

    user.status = data.get("status")

    db.session.commit()


def get_all_users():
    return User.query.all()


def get_user(
    user_id: int,
    options: list = None,
    active_check: bool = True,
    blocked_check: bool = True,
) -> User:

    query = User.query

    if options is not None:
        query = query.options(*options)

    user = query.get(user_id)

    if user is None:
        raise DefaultException("user_not_found", code=404)

    if active_check and user.status == "waitActivation":
        raise DefaultException("user_not_activated", code=409)
    if blocked_check and user.status == "blocked":
        raise DefaultException("user_is_blocked", code=409)

    return user


from app.main.service.email_service import send_email_activation
from app.main.service.password_service import hash_password, token_generate
from app.main.service.professional_service import get_professional
