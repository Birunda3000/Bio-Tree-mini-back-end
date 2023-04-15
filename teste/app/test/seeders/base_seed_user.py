from time import time

from app.main.model import User
from app.main.service import hash_password


def create_base_seed_user(db):
    new_user = User(
        professional_id=1,
        login="user@uece.br",
        password=hash_password("aaaaaaaaa"),
        activation_token="test",
        activation_token_exp=int(time()) + 300,
        reset_password_token="test",
        reset_password_token_exp=int(time()) + 300,
        status="waitActivation",
    )

    db.session.add(new_user)

    new_user = User(
        professional_id=2,
        login="user1@uece.br",
        password=hash_password("bbbbbbbbb"),
        activation_token="test1",
        activation_token_exp=0,
        reset_password_token="test1",
        reset_password_token_exp=int(time()) + 300,
        status="active",
    )

    db.session.add(new_user)

    new_user = User(
        professional_id=10,
        login="user2@uece.br",
        password=hash_password("ccccccccc"),
        activation_token="test2",
        activation_token_exp=int(time()) + 300,
        reset_password_token="test2",
        reset_password_token_exp=int(time()) + 300,
        status="waitActivation",
    )

    db.session.add(new_user)

    new_user = User(
        professional_id=4,
        login="user3@uece.br",
        password=hash_password(""),
        activation_token="test3",
        activation_token_exp=0,
        reset_password_token="test3",
        reset_password_token_exp=0,
        status="active",
    )

    db.session.add(new_user)

    new_user = User(
        professional_id=5,
        login="user4@uece.br",
        password=hash_password("teste"),
        activation_token="test4",
        activation_token_exp=int(time()) + 300,
        reset_password_token="test4",
        reset_password_token_exp=int(time()) + 300,
        status="blocked",
    )

    db.session.add(new_user)

    new_user = User(
        professional_id=6,
        login="user5@uece.br",
        password=hash_password(""),
        activation_token="test5",
        activation_token_exp=0,
        reset_password_token="test5",
        reset_password_token_exp=int(time()) + 300,
        status="waitActivation",
    )

    db.session.add(new_user)

    new_user = User(
        professional_id=7,
        login="user6@uece.br",
        password=hash_password(""),
        activation_token="test6",
        activation_token_exp=int(time()) + 300,
        reset_password_token="test6",
        reset_password_token_exp=int(time()) + 300,
        status="waitActivation",
    )

    db.session.add(new_user)

    new_user = User(
        professional_id=8,
        login="user7@uece.br",
        password=hash_password("testeteste"),
        activation_token="test7",
        activation_token_exp=int(time()) + 300,
        reset_password_token="test7",
        reset_password_token_exp=int(time()) + 300,
        status="active",
    )

    db.session.add(new_user)

    new_user = User(
        professional_id=9,
        login="user8@uece.br",
        password=hash_password("testeteste"),
        activation_token="test8",
        activation_token_exp=0,
        reset_password_token="test8",
        reset_password_token_exp=0,
        status="active",
    )

    db.session.add(new_user)

    db.session.commit()
