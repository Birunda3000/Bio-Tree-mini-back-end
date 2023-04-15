from math import ceil

from sqlalchemy.orm import joinedload
from werkzeug.datastructures import ImmutableMultiDict

from app.main import db
from app.main.config import Config
from app.main.exceptions import DefaultException
from app.main.model import Equipment

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def get_equipments(params: ImmutableMultiDict) -> list[Equipment]:

    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)
    name = params.get("name", type=str)
    filters = []

    if name:
        filters.append(Equipment.name.ilike(f"%{name.upper()}%"))

    pagination = (
        Equipment.query.options(joinedload("equipment_type"))
        .filter(*filters)
        .order_by(Equipment.id)
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return {
        "current_page": page,
        "total_items": pagination.total,
        "total_pages": ceil(pagination.total / per_page),
        "items": pagination.items,
    }


def save_new_equipment(data: dict[str, any]) -> None:
    name = data.get("name")

    equipment_type = get_equipment_type(equipment_type_id=data.get("equipment_type_id"))

    if _equipment_exists(name=name):
        raise DefaultException("name_in_use", code=409)

    new_equipment = Equipment(name=name, equipment_type=equipment_type)

    db.session.add(new_equipment)
    db.session.commit()


def delete_equipment(equipment_id: int):

    equipment = get_equipment(equipment_id=equipment_id)

    db.session.delete(equipment)
    db.session.commit()


def get_equipment(equipment_id: int, options: list = None) -> Equipment:

    query = Equipment.query

    if options is not None:
        query = query.options(*options)

    equipment = query.get(equipment_id)

    if equipment is None:
        raise DefaultException("equipment_not_found", code=404)

    return equipment


def _equipment_exists(name: str) -> bool:
    return (
        Equipment.query.with_entities(Equipment.id)
        .filter(Equipment.name == name.upper())
        .scalar()
        is not None
    )


from app.main.service.equipment.equipment_type_service import get_equipment_type
