from math import ceil

from werkzeug.datastructures import ImmutableMultiDict

from app.main import db
from app.main.config import Config
from app.main.exceptions import DefaultException
from app.main.model import UnitMeasurement

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def get_unit_measurements(params: ImmutableMultiDict):

    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)
    name = params.get("name", type=str)

    filters = []

    if name:
        filters.append(UnitMeasurement.name.ilike(f"%{name.upper()}%"))

    pagination = (
        UnitMeasurement.query.filter(*filters)
        .order_by(UnitMeasurement.id)
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return {
        "current_page": page,
        "total_items": pagination.total,
        "total_pages": ceil(pagination.total / per_page),
        "items": pagination.items,
    }


def save_new_unit_measurement(data: dict[str, any]) -> None:

    name = data.get("name")

    if _unit_measurement_exists(name):
        raise DefaultException("name_in_use", code=409)

    new_unit_measurement = UnitMeasurement(name=name)

    db.session.add(new_unit_measurement)
    db.session.commit()


def update_unit_measurement(unit_measurement_id: int, data: dict[str, str]) -> None:

    unit_measurement = get_unit_measurement(unit_measurement_id=unit_measurement_id)

    new_name = data.get("name").upper()

    if unit_measurement.name != new_name and _unit_measurement_exists(new_name):
        raise DefaultException("name_in_use", code=409)

    unit_measurement.name = new_name

    db.session.commit()


def delete_unit_measurement(unit_measurement_id: int):

    unit_measurement = get_unit_measurement(unit_measurement_id=unit_measurement_id)

    db.session.delete(unit_measurement)
    db.session.commit()


def get_unit_measurement(
    unit_measurement_id: int, options: list = None
) -> UnitMeasurement:

    query = UnitMeasurement.query

    if options is not None:
        query = query.options(*options)

    unit_measurement = query.get(unit_measurement_id)

    if unit_measurement is None:
        raise DefaultException("unit_measurement_not_found", code=404)

    return unit_measurement


def _unit_measurement_exists(unit_measurement_name: str) -> bool:
    return (
        UnitMeasurement.query.with_entities(UnitMeasurement.id)
        .filter(UnitMeasurement.name == unit_measurement_name.upper())
        .scalar()
        is not None
    )
