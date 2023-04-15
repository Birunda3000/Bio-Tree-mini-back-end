from math import ceil

from sqlalchemy import or_
from sqlalchemy.orm import joinedload
from werkzeug.datastructures import ImmutableMultiDict

from app.main import db
from app.main.config import Config
from app.main.exceptions import DefaultException
from app.main.model import Classification, Service

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def get_services(params: ImmutableMultiDict):

    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)
    name = params.get("name", type=str)
    code = params.get("code", type=str)

    filters = []

    if name:
        filters.append(Service.name.ilike(f"%{name}%"))
    if code:
        filters.append(Service.code.ilike(f"%{code}%"))

    pagination = (
        Service.query.filter(*filters)
        .order_by(Service.id)
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return {
        "current_page": page,
        "total_items": pagination.total,
        "total_pages": ceil(pagination.total / per_page),
        "items": pagination.items,
    }


def save_new_service(data: dict[str, any]) -> None:

    code = data.get("code")
    name = data.get("name").upper()

    filters = [
        or_(Service.name == name, Service.code == code),
    ]

    _check_if_service_already_exists(filters=filters, name=name)

    new_service = Service(code=code, name=name)

    db.session.add(new_service)
    db.session.commit()


def update_service(service_id: int, data: dict[str, str]) -> None:

    service = get_service(service_id=service_id)

    new_code = data.get("code")
    new_name = data.get("name").upper()

    filters = []

    if change_code := service.code != new_code:
        filters.append(Service.code == new_code)

    if change_name := service.name != new_name:
        filters.append(Service.name == new_name)

    if change_code or change_name:
        filters = [Service.id != service.id, or_(*filters)]

        _check_if_service_already_exists(filters=filters, name=new_name)

    service.code = new_code
    service.name = new_name

    db.session.commit()


def delete_service(service_id: int):

    service = get_service(service_id=service_id)

    if Classification.query.filter(Classification.service_id == service_id).first():
        raise DefaultException("service_is_associated_with_classification", code=409)

    db.session.delete(service)
    db.session.commit()


def get_service(service_id: int) -> Service:

    service = (
        Service.query.filter(Service.id == service_id)
        .options(joinedload("classifications"))
        .first()
    )

    if service is None:
        raise DefaultException("service_not_found", code=404)

    return service


def service_exists(
    service_code: str, service_name: str, service_id: int = None
) -> bool:

    filters = []
    if service_id:
        filters.append(Service.id != service_id)

    return (
        Service.query.with_entities(Service.id)
        .filter(
            or_(Service.name == service_name, Service.code == service_code),
            *filters,
        )
        .scalar()
        is not None
    )


def _check_if_service_already_exists(filters: list[any], name: str):
    if (
        service := Service.query.with_entities(Service.name, Service.code)
        .filter(*filters)
        .first()
    ):
        if service.name == name:
            raise DefaultException("name_in_use", code=409)
        else:
            raise DefaultException("code_in_use", code=409)
