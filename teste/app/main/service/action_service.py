from math import ceil

from sqlalchemy import or_
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from werkzeug.datastructures import ImmutableMultiDict

from app.main import db
from app.main.config import Config
from app.main.exceptions import DefaultException
from app.main.model import Action

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def get_actions(params: ImmutableMultiDict):

    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)
    name = params.get("name", type=str)

    filters = []

    if name:
        filters.append(Action.name.ilike(f"%{name.upper()}%"))

    pagination = (
        Action.query.filter(*filters)
        .order_by(Action.id)
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return {
        "current_page": page,
        "total_items": pagination.total,
        "total_pages": ceil(pagination.total / per_page),
        "items": pagination.items,
    }


def save_new_action(data: dict[str, any]):

    name = data.get("name")

    if _action_exists(action_name=name):
        raise DefaultException("name_in_use", code=409)

    new_action = Action(name=name)

    db.session.add(new_action)
    db.session.commit()


def update_action(action_id: int, data: dict[str, any]) -> None:

    name = data.get("name").upper()

    filters = [
        or_(
            Action.id == action_id,
            Action.name == name,
        )
    ]

    try:
        action = Action.query.filter(*filters).one()
    except MultipleResultsFound:
        raise DefaultException("name_in_use", code=409)
    except NoResultFound:
        raise DefaultException("action_not_found", code=404)

    if action.id != action_id:
        raise DefaultException("action_not_found", code=404)

    action.name = name

    db.session.commit()


def delete_action(action_id: int) -> None:

    action = get_action(action_id=action_id)

    filters = [Action.id == action_id]

    if Action.query.with_entities(Action.prescriptions.any()).filter(*filters).scalar():
        raise DefaultException("action_is_associated_with_prescription", code=409)

    db.session.delete(action)
    db.session.commit()


def get_action(action_id: int, options: list = None) -> Action:

    query = Action.query

    if options is not None:
        query = query.options(*options)

    action = query.get(action_id)

    if action is None:
        raise DefaultException("action_not_found", code=404)

    return action


def _action_exists(action_name: str) -> bool:

    return (
        Action.query.with_entities(Action.id)
        .filter(Action.name == action_name.upper())
        .scalar()
        is not None
    )
