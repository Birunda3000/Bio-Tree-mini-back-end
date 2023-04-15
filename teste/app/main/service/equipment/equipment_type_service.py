from math import ceil

from werkzeug.datastructures import ImmutableMultiDict

from app.main import db
from app.main.config import Config
from app.main.exceptions import DefaultException
from app.main.model import EquipmentType

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def get_equipment_types(params: ImmutableMultiDict):
    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)
    name = params.get("name", type=str)

    filters = []

    if name:
        filters.append(EquipmentType.name.ilike(f"%{name.upper()}%"))

    pagination = (
        EquipmentType.query.filter(*filters)
        .order_by(EquipmentType.id)
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return {
        "current_page": page,
        "total_items": pagination.total,
        "total_pages": ceil(pagination.total / per_page),
        "items": pagination.items,
    }


def save_new_equipment_type(data: dict[str, any]) -> None:
    name = data.get("name")

    if _equipment_type_exists(name=name):
        raise DefaultException("name_in_use", code=409)

    new_equipment_type = EquipmentType(name=name)

    db.session.add(new_equipment_type)
    db.session.commit()


def update_equipment_type(equipment_type_id: int, data: dict[str, str]) -> None:
    equipment_type = get_equipment_type(equipment_type_id=equipment_type_id)

    new_name = data.get("name").upper()

    if equipment_type.name != new_name and _equipment_type_exists(new_name):
        raise DefaultException("name_in_use", code=409)

    equipment_type.name = new_name

    db.session.commit()


def delete_equipment_type(equipment_type_id: int):
    filters = [EquipmentType.id == equipment_type_id]

    if (
        EquipmentType.query.with_entities(EquipmentType.equipments.any())
        .filter(*filters)
        .scalar()
    ):
        raise DefaultException("equipment_type_is_associated_with_equipment", code=409)

    equipment_type = get_equipment_type(equipment_type_id=equipment_type_id)

    db.session.delete(equipment_type)
    db.session.commit()


def get_equipment_type(equipment_type_id: int, options: list = None) -> EquipmentType:

    query = EquipmentType.query

    if options is not None:
        query = query.options(*options)

    equipment_type = query.get(equipment_type_id)

    if equipment_type is None:
        raise DefaultException("equipment_type_not_found", code=404)

    return equipment_type


def _equipment_type_exists(name: str) -> bool:
    return (
        EquipmentType.query.with_entities(EquipmentType.id)
        .filter(EquipmentType.name == name.upper())
        .scalar()
        is not None
    )
