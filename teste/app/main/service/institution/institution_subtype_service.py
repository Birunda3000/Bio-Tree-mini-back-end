from math import ceil

from werkzeug.datastructures import ImmutableMultiDict

from app.main import db
from app.main.config import Config
from app.main.exceptions import DefaultException
from app.main.model import InstitutionSubtype
from app.main.service.institution.institution_type_service import get_institution_type

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def get_institution_subtypes(params: ImmutableMultiDict):

    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)
    name = params.get("name", type=str)
    institution_type_id = params.get("institution_type_id", type=int)

    filters = []

    if name:
        filters.append(InstitutionSubtype.name.ilike(f"%{name.upper()}%"))
    if institution_type_id:
        filters.append(InstitutionSubtype.institution_type_id == institution_type_id)

    pagination = (
        InstitutionSubtype.query.filter(*filters)
        .order_by(InstitutionSubtype.id)
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return {
        "current_page": page,
        "total_items": pagination.total,
        "total_pages": ceil(pagination.total / per_page),
        "items": pagination.items,
    }


def save_new_institution_subtype(data: dict[str, any]) -> None:

    institution_type_id = int(data.get("institution_type_id"))
    get_institution_type(institution_type_id=institution_type_id)

    name = data.get("name")
    if _institution_subtype_exists(
        institution_type_id=institution_type_id,
        institution_subtype_name=name,
    ):
        raise DefaultException("name_in_use", code=409)

    new_institution_subtype = InstitutionSubtype(
        institution_type_id=institution_type_id,
        name=name,
    )

    db.session.add(new_institution_subtype)
    db.session.commit()


def update_institution_subtype(
    institution_subtype_id: int, data: dict[str, str]
) -> None:

    institution_subtype = get_institution_subtype(
        institution_subtype_id=institution_subtype_id
    )

    new_institution_type_id = data.get("institution_type_id")
    if new_institution_type_id is not None:
        get_institution_type(institution_type_id=new_institution_type_id)
        institution_subtype.institution_type_id = new_institution_type_id

    new_name = data.get("name").upper()

    if institution_subtype.name != new_name and _institution_subtype_exists(
        institution_type_id=institution_subtype.institution_type_id,
        institution_subtype_name=new_name,
    ):
        raise DefaultException("name_in_use", code=409)

    institution_subtype.name = new_name

    db.session.commit()


def delete_institution_subtype(institution_subtype_id: int):

    institution_subtype = get_institution_subtype(
        institution_subtype_id=institution_subtype_id
    )

    db.session.delete(institution_subtype)
    db.session.commit()


def get_institution_subtype(
    institution_subtype_id: int, options: list = None
) -> InstitutionSubtype:

    query = InstitutionSubtype.query

    if options is not None:
        query = query.options(*options)

    institution_subtype = query.get(institution_subtype_id)

    if institution_subtype is None:
        raise DefaultException("institution_subtype_not_found", code=404)

    return institution_subtype


def _institution_subtype_exists(
    institution_type_id: int, institution_subtype_name: str
) -> bool:
    return (
        InstitutionSubtype.query.with_entities(InstitutionSubtype.id)
        .filter(
            InstitutionSubtype.name == institution_subtype_name.upper(),
            InstitutionSubtype.institution_type_id == institution_type_id,
        )
        .scalar()
        is not None
    )
