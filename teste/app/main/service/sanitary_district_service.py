from math import ceil

from sqlalchemy import and_
from werkzeug.datastructures import ImmutableMultiDict

from app.main import db
from app.main.config import Config
from app.main.exceptions import DefaultException
from app.main.model import SanitaryDistrict

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def get_sanitary_districts(params: ImmutableMultiDict) -> list[SanitaryDistrict]:

    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)
    name = params.get("name", type=str)

    filters = []

    if name:
        filters.append(SanitaryDistrict.name.ilike(f"%{name.upper()}%"))

    pagination = (
        SanitaryDistrict.query.filter(*filters)
        .order_by(SanitaryDistrict.id)
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return {
        "current_page": page,
        "total_items": pagination.total,
        "total_pages": ceil(pagination.total / per_page),
        "items": pagination.items,
    }


def save_new_sanitary_district(data: dict[str, any]) -> None:

    name = data.get("name").upper()

    if _sanitary_district_exists(sanitary_district_name=name):
        raise DefaultException("name_in_use", code=409)

    new_sanitary_district = SanitaryDistrict(name=name)

    db.session.add(new_sanitary_district)
    db.session.commit()


def update_sanitary_district(sanitary_district_id: int, data: dict[str, str]) -> None:

    sanitary_district = get_sanitary_district(sanitary_district_id=sanitary_district_id)

    name = data.get("name").upper()

    if _sanitary_district_exists(
        sanitary_district_id=sanitary_district.id, sanitary_district_name=name
    ):
        raise DefaultException("name_in_use", code=409)

    sanitary_district.name = name

    db.session.commit()


def delete_sanitary_district(sanitary_district_id: int) -> None:
    sanitary_district = get_sanitary_district(sanitary_district_id=sanitary_district_id)

    db.session.delete(sanitary_district)
    db.session.commit()


def get_sanitary_district(sanitary_district_id: int) -> SanitaryDistrict:

    sanitary_district = SanitaryDistrict.query.filter(
        SanitaryDistrict.id == sanitary_district_id
    ).first()

    if sanitary_district is None:
        raise DefaultException("sanitary_district_not_found", code=404)

    return sanitary_district


def _sanitary_district_exists(
    sanitary_district_name: str, sanitary_district_id: int = None
) -> bool:

    filters = []
    if sanitary_district_id:
        filters.append(SanitaryDistrict.id != sanitary_district_id)

    return (
        SanitaryDistrict.query.with_entities(SanitaryDistrict.id)
        .filter(and_(SanitaryDistrict.name == sanitary_district_name, *filters))
        .scalar()
        is not None
    )
