from math import ceil

from sqlalchemy import or_
from sqlalchemy.engine.row import Row
from werkzeug.datastructures import ImmutableMultiDict

from app.main import db
from app.main.config import Config
from app.main.exceptions import DefaultException
from app.main.model import Enablement

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def get_enablements(params: ImmutableMultiDict):

    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)
    name = params.get("name", type=str)
    code = params.get("code", type=str)

    filters = []

    if name:
        filters.append(Enablement.name.ilike(f"%{name.upper()}%"))

    if code:
        filters.append(Enablement.code.ilike(f"%{code}%"))

    pagination = (
        Enablement.query.filter(*filters)
        .order_by(Enablement.id)
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return {
        "current_page": page,
        "total_items": pagination.total,
        "total_pages": ceil(pagination.total / per_page),
        "items": pagination.items,
    }


def save_new_enablement(data: dict[str, any]) -> None:

    name = data.get("name").upper()
    code = data.get("code")
    release_date = data.get("release_date")

    if enablement := _enablement_exists(enablement_name=name, enablement_code=code):
        if enablement.name == name:
            raise DefaultException("name_in_use", code=409)
        else:
            raise DefaultException("code_in_use", code=409)

    new_enablement = Enablement(
        code=code,
        name=name,
        number_of_beds=data.get("number_of_beds"),
        ordinance_number=data.get("ordinance_number"),
        release_date=date_from_string(release_date) if release_date else None,
    )

    db.session.add(new_enablement)
    db.session.commit()


def delete_enablement(enablement_id: int):

    enablement = get_enablement(enablement_id=enablement_id)

    db.session.delete(enablement)
    db.session.commit()


def get_enablement(enablement_id: int, options: list = None) -> Enablement:

    query = Enablement.query

    if options is not None:
        query = query.options(*options)

    enablement = query.get(enablement_id)

    if enablement is None:
        raise DefaultException("enablement_not_found", code=404)

    return enablement


def _enablement_exists(enablement_name: str, enablement_code: str) -> Row:
    return (
        Enablement.query.with_entities(Enablement.name, Enablement.code)
        .filter(
            or_(
                Enablement.name == enablement_name,
                Enablement.code == enablement_code,
            )
        )
        .first()
    )


from app.main.service import date_from_string
