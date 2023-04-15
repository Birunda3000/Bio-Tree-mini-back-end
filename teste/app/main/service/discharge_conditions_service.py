from math import ceil

from sqlalchemy import or_
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from werkzeug.datastructures import ImmutableMultiDict

from app.main import db
from app.main.config import Config
from app.main.exceptions import DefaultException
from app.main.model import DischargeCondition

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def get_all_discharge_conditions(
    params: ImmutableMultiDict,
) -> list[DischargeCondition]:
    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)
    name = params.get("name", default=None)

    filters = []
    if name:
        filters.append(DischargeCondition.name.ilike(f"%{name}%"))

    pagination = (
        DischargeCondition.query.filter(*filters)
        .order_by(DischargeCondition.id)
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return {
        "current_page": page,
        "total_items": pagination.total,
        "total_pages": ceil(pagination.total / per_page),
        "items": pagination.items,
    }


def get_discharge_condition_by_id(discharge_condition_id: int) -> DischargeCondition:
    return get_discharge_condition(discharge_condition_id=discharge_condition_id)


def save_discharge_condition(data: dict[str, any]):
    if discharge_condition := DischargeCondition.query.filter_by(
        name=data.get("name")
    ).first():
        raise DefaultException("name_in_use", code=409)
    new_discharge_condition = DischargeCondition(name=data.get("name"))

    db.session.add(new_discharge_condition)
    db.session.commit()


def update_discharge_condition(
    discharge_condition_id: int, data: dict[str, any]
) -> None:
    filters = [
        or_(
            DischargeCondition.id == discharge_condition_id,
            DischargeCondition.name == data.get("name"),
        )
    ]
    try:
        discharge_condition = DischargeCondition.query.filter(*filters).one()
    except MultipleResultsFound:
        raise DefaultException("name_in_use", code=409)
    except NoResultFound:
        raise DefaultException("discharge_condition_not_found", code=404)
    if discharge_condition.id != discharge_condition_id:
        raise DefaultException("discharge_condition_not_found", code=404)
    discharge_condition.name = data.get("name")

    db.session.commit()


def delete_discharge_condition(discharge_condition_id: int) -> None:
    discharge_condition = get_discharge_condition(
        discharge_condition_id=discharge_condition_id
    )
    db.session.delete(discharge_condition)
    db.session.commit()


def get_discharge_condition(
    discharge_condition_id: int, options: list = None
) -> DischargeCondition:

    query = DischargeCondition.query

    if options is not None:
        query = query.options(*options)

    discharge_condition = query.get(discharge_condition_id)

    if discharge_condition is None:
        raise DefaultException("discharge_condition_not_found", code=404)

    return discharge_condition
