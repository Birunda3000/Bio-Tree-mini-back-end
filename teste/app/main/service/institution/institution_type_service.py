from math import ceil

from sqlalchemy.orm import joinedload
from werkzeug.datastructures import ImmutableMultiDict

from app.main import db
from app.main.config import Config
from app.main.exceptions import DefaultException
from app.main.model import InstitutionSubtype, InstitutionType

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def get_institution_types(params: ImmutableMultiDict):

    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)
    name = params.get("name", type=str)

    filters = []

    if name:
        filters.append(InstitutionType.name.ilike(f"%{name.upper()}%"))

    pagination = (
        InstitutionType.query.filter(*filters)
        .order_by(InstitutionType.id)
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return {
        "current_page": page,
        "total_items": pagination.total,
        "total_pages": ceil(pagination.total / per_page),
        "items": pagination.items,
    }


def save_new_institution_type(data: dict[str, any]) -> None:

    name = data.get("name")

    if _institution_type_exists(name):
        raise DefaultException("name_in_use", code=409)

    new_institution_type = InstitutionType(name=name)

    db.session.add(new_institution_type)
    db.session.commit()


def update_institution_type(institution_type_id: int, data: dict[str, str]) -> None:

    institution_type = get_institution_type(
        institution_type_id=institution_type_id, options=None
    )

    new_name = data.get("name").upper()

    if institution_type.name != new_name and _institution_type_exists(new_name):
        raise DefaultException("name_in_use", code=409)

    institution_type.name = new_name

    db.session.commit()


def delete_institution_type(institution_type_id: int):

    institution_type = get_institution_type(
        institution_type_id=institution_type_id, options=None
    )

    if InstitutionSubtype.query.filter(
        InstitutionSubtype.institution_type_id == institution_type_id
    ).first():
        raise DefaultException("institution_type_is_associated_with_subtype", code=409)

    db.session.delete(institution_type)
    db.session.commit()


def get_institution_type(
    institution_type_id: int, options: list = [joinedload("institution_subtypes")]
) -> InstitutionType:

    query = InstitutionType.query

    if options is not None:
        query = query.options(*options)

    institution_type = query.get(institution_type_id)

    if institution_type is None:
        raise DefaultException("institution_type_not_found", code=404)

    return institution_type


def _institution_type_exists(institution_type_name: str) -> bool:
    return (
        InstitutionType.query.with_entities(InstitutionType.id)
        .filter(InstitutionType.name == institution_type_name.upper())
        .scalar()
        is not None
    )
