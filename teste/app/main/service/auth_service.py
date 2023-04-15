from datetime import datetime, timedelta
from functools import wraps
from typing import Dict

import bcrypt
import jwt
from flask import jsonify, make_response, request

from app.main.config import app_config
from app.main.exceptions import DefaultException
from app.main.model import Professional, User

_secret_key = app_config.SECRET_KEY
_jwt_exp = app_config.JWT_EXP


def hash_password(password: str) -> str:

    password = password.encode("utf-8")
    return bcrypt.hashpw(password, bcrypt.gensalt()).decode("utf-8")


def check_pw(p1: str, p2: str) -> bool:

    p1 = p1.encode("utf-8")
    p2 = p2.encode("utf-8")
    return bcrypt.checkpw(p1, p2)


def login(data: Dict[str, any]) -> str:

    user = User.query.filter_by(login=data.get("login")).scalar()

    if not user:
        raise DefaultException(message="password_incorrect_information", code=401)

    if not user.status == "active":
        raise DefaultException("user_not_activated", code=409)

    login_pwd = data.get("password")
    user_pwd = user.password

    if not check_pw(login_pwd, user_pwd):
        raise DefaultException("password_incorrect_information", code=401)

    professional = get_professional(professional_id=user.professional_id)

    token = create_jwt(user.id)
    return "Bearer " + token, professional


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
            token = token.replace("Bearer ", "")
        if not token:
            return make_response(jsonify({"errors": "token_invalid!"}), 401)
        try:
            data = jwt.decode(token, _secret_key, algorithms=["HS256"])
        except:
            return make_response(jsonify({"errors": "token_invalid!"}), 401)
        return f(*args, **kwargs)

    return decorator


def create_jwt(sub: int):

    return jwt.encode(
        {"sub": sub, "exp": datetime.utcnow() + timedelta(hours=_jwt_exp)}, _secret_key
    )


from app.main.service.professional_service import get_professional
