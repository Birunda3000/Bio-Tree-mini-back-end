from math import ceil

from psycopg2 import errors
from sqlalchemy.exc import IntegrityError
from werkzeug.datastructures import ImmutableMultiDict

from app.main import app, db
from app.main.config import Config
from app.main.exceptions import DefaultException
from app.main.model import Cooperative

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def get_cooperatives(params: ImmutableMultiDict):

    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)
    cbo = params.get("cbo", type=str)

    filters = []

    if cbo:
        filters.append(Cooperative.cbo.ilike(f"%{cbo.upper()}%"))

    pagination = (
        Cooperative.query.filter(*filters)
        .order_by(Cooperative.id)
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return {
        "current_page": page,
        "total_items": pagination.total,
        "total_pages": ceil(pagination.total / per_page),
        "items": pagination.items,
    }


def save_new_cooperative(data: dict[str, any]) -> None:

    cbo = data.get("cbo")

    if _cooperative_exists(cooperative_cbo=cbo):
        raise DefaultException("cbo_in_use", code=409)

    new_cooperative = Cooperative(name=data.get("name"), cbo=cbo)

    db.session.add(new_cooperative)
    db.session.commit()


def update_cooperative(cooperative_id: int, data: dict[str, str]) -> None:

    cooperative = get_cooperative(cooperative_id=cooperative_id)

    cbo = data.get("cbo")

    if cooperative.cbo != cbo and _cooperative_exists(cooperative_cbo=cbo):
        raise DefaultException("cbo_in_use", code=409)

    cooperative.name = data.get("name")
    cooperative.cbo = cbo

    db.session.commit()


def delete_cooperative(cooperative_id: int):

    cooperative = get_cooperative(cooperative_id=cooperative_id)

    db.session.delete(cooperative)
    db.session.commit()


def get_cooperative(cooperative_id: int, options: list = None) -> Cooperative:

    query = Cooperative.query

    if options is not None:
        query = query.options(*options)

    cooperative = query.get(cooperative_id)

    if cooperative is None:
        raise DefaultException("cooperative_not_found", code=404)

    return cooperative


def _cooperative_exists(cooperative_cbo: str) -> bool:
    return (
        Cooperative.query.with_entities(Cooperative.id)
        .filter(Cooperative.cbo == cooperative_cbo)
        .scalar()
        is not None
    )
