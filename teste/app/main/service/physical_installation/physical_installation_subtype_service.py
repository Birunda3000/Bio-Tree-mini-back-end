from math import ceil

from werkzeug.datastructures import ImmutableMultiDict

from app.main import db
from app.main.config import Config
from app.main.exceptions import DefaultException
from app.main.model import PhysicalInstallationSubtype

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def get_physical_installation_subtypes(params: ImmutableMultiDict):

    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)
    name = params.get("name", type=str)

    filters = []

    if name:
        filters.append(PhysicalInstallationSubtype.name.ilike(f"%{name.upper()}%"))

    pagination = (
        PhysicalInstallationSubtype.query.filter(*filters)
        .order_by(PhysicalInstallationSubtype.id)
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return {
        "current_page": page,
        "total_items": pagination.total,
        "total_pages": ceil(pagination.total / per_page),
        "items": pagination.items,
    }


def get_physical_installation_subtype_by_id(
    physical_installation_subtype_id: int,
) -> PhysicalInstallationSubtype:
    return get_physical_installation_subtype(
        physical_installation_subtype_id=physical_installation_subtype_id
    )


def save_new_physical_installation_subtype(data: dict[str, any]):

    name = data.get("name").upper()

    _verify_unique_data(physical_installation_subtype_name=name)

    new_physical_installation_subtype = PhysicalInstallationSubtype(name=name)

    db.session.add(new_physical_installation_subtype)
    db.session.commit()


def update_physical_installation_subtype(
    physical_installation_subtype_id: int, data: dict[str, any]
) -> None:

    physical_installation_subtype = get_physical_installation_subtype(
        physical_installation_subtype_id=physical_installation_subtype_id
    )

    name = data.get("name").upper()

    if name != physical_installation_subtype.name:
        _verify_unique_data(
            physical_installation_subtype_name=name,
            filters=[
                PhysicalInstallationSubtype.id != physical_installation_subtype.id
            ],
        )

        physical_installation_subtype.name = name

        db.session.commit()


def delete_physical_installation_subtype(physical_installation_subtype_id: int) -> None:

    physical_installation_subtype = get_physical_installation_subtype(
        physical_installation_subtype_id=physical_installation_subtype_id
    )

    db.session.delete(physical_installation_subtype)
    db.session.commit()


def get_physical_installation_subtype(
    physical_installation_subtype_id: int, options: list = None
) -> PhysicalInstallationSubtype:

    query = PhysicalInstallationSubtype.query

    if options is not None:
        query = query.options(*options)

    physical_installation_subtype = query.get(physical_installation_subtype_id)

    if physical_installation_subtype is None:
        raise DefaultException("physical_installation_subtype_not_found", code=404)

    return physical_installation_subtype


def _verify_unique_data(physical_installation_subtype_name: str, filters: list = []):

    if (
        PhysicalInstallationSubtype.query.with_entities(
            PhysicalInstallationSubtype.name
        )
        .filter(
            PhysicalInstallationSubtype.name == physical_installation_subtype_name,
            *filters,
        )
        .first()
    ):
        raise DefaultException("name_in_use", code=409)
