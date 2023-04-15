from math import ceil

from werkzeug.datastructures import ImmutableMultiDict

from app.main import db
from app.main.config import Config
from app.main.exceptions import DefaultException
from app.main.model import PhysicalInstallationType

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def get_physical_installation_types(params: ImmutableMultiDict):

    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)
    name = params.get("name", type=str)

    filters = []

    if name:
        filters.append(PhysicalInstallationType.name.ilike(f"%{name.upper()}%"))

    pagination = (
        PhysicalInstallationType.query.filter(*filters)
        .order_by(PhysicalInstallationType.id)
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return {
        "current_page": page,
        "total_items": pagination.total,
        "total_pages": ceil(pagination.total / per_page),
        "items": pagination.items,
    }


def get_physical_installation_type_by_id(
    physical_installation_type_id: int,
) -> PhysicalInstallationType:
    return get_physical_installation_type(
        physical_installation_type_id=physical_installation_type_id,
    )


def save_new_physical_installation_type(data: dict[str, any]):

    name = data.get("name").upper()

    _verify_unique_data(physical_installation_type_name=name)

    new_physical_installation_type = PhysicalInstallationType(name=name)

    db.session.add(new_physical_installation_type)
    db.session.commit()


def update_physical_installation_type(
    physical_installation_type_id: int, data: dict[str, any]
) -> None:

    physical_installation_type = get_physical_installation_type(
        physical_installation_type_id=physical_installation_type_id
    )

    name = data.get("name").upper()

    if name != physical_installation_type.name:
        _verify_unique_data(
            physical_installation_type_name=name,
            filters=[PhysicalInstallationType.id != physical_installation_type.id],
        )

        physical_installation_type.name = name

        db.session.commit()


def delete_physical_installation_type(physical_installation_type_id: int) -> None:

    physical_installation_type = get_physical_installation_type(
        physical_installation_type_id=physical_installation_type_id
    )

    db.session.delete(physical_installation_type)
    db.session.commit()


def get_physical_installation_type(
    physical_installation_type_id: int, options: list = None
) -> PhysicalInstallationType:

    query = PhysicalInstallationType.query

    if options is not None:
        query = query.options(*options)

    physical_installation_type = query.get(physical_installation_type_id)

    if physical_installation_type is None:
        raise DefaultException("physical_installation_type_not_found", code=404)

    return physical_installation_type


def _verify_unique_data(physical_installation_type_name: str, filters: list = []):

    if (
        PhysicalInstallationType.query.with_entities(PhysicalInstallationType.name)
        .filter(
            PhysicalInstallationType.name == physical_installation_type_name,
            *filters,
        )
        .first()
    ):
        raise DefaultException("name_in_use", code=409)
