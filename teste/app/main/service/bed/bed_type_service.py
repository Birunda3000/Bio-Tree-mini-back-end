from math import ceil

from werkzeug.datastructures import ImmutableMultiDict

from app.main import db
from app.main.config import Config
from app.main.exceptions import DefaultException
from app.main.model import BedType

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def get_bed_types(params: ImmutableMultiDict):

    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)
    name = params.get("name", type=str)

    filters = []

    if name:
        filters.append(BedType.name.ilike(f"%{name.upper()}%"))

    pagination = (
        BedType.query.filter(*filters)
        .order_by(BedType.id)
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return {
        "current_page": page,
        "total_items": pagination.total,
        "total_pages": ceil(pagination.total / per_page),
        "items": pagination.items,
    }


def save_new_bed_type(data: dict[str, any]) -> None:

    name = data.get("name").upper()

    if _bed_type_exists(name=name):
        raise DefaultException("name_in_use", code=409)

    new_bed_type = BedType(
        name=name,
    )

    db.session.add(new_bed_type)
    db.session.commit()


def update_bed_type(bed_type_id: int, data: dict[str, str]) -> None:

    bed_type = get_bed_type(bed_type_id=bed_type_id)

    new_name = data.get("name").upper()

    if new_name != bed_type.name and _bed_type_exists(name=new_name):
        raise DefaultException("name_in_use", code=409)

    bed_type.name = data.get("name")

    db.session.commit()


def delete_bed_type(bed_type_id: int):

    bed_type = get_bed_type(bed_type_id=bed_type_id)

    db.session.delete(bed_type)
    db.session.commit()


def get_bed_type(bed_type_id: int, options: list = None) -> BedType:

    query = BedType.query

    if options is not None:
        query = query.options(*options)

    bed_type = query.get(bed_type_id)

    if bed_type is None:
        raise DefaultException("bed_type_not_found", code=404)

    return bed_type


def _bed_type_exists(name: str) -> bool:
    return (
        BedType.query.with_entities(BedType.id).filter(BedType.name == name).scalar()
        is not None
    )
