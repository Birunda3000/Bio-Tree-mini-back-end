from math import ceil

from werkzeug.datastructures import ImmutableMultiDict

from app.main import db
from app.main.config import Config
from app.main.exceptions import DefaultException
from app.main.model import Medicine

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def get_medicines(params: ImmutableMultiDict):

    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)
    name = params.get("name", type=str)

    filters = []

    if name:
        filters.append(Medicine.name.ilike(f"%{name}%"))

    pagination = (
        Medicine.query.filter(*filters)
        .order_by(Medicine.id)
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return {
        "current_page": page,
        "total_items": pagination.total,
        "total_pages": ceil(pagination.total / per_page),
        "items": pagination.items,
    }


def save_new_medicine(data: dict[str, str]) -> None:

    new_medicine = Medicine(name=data.get("name"))

    db.session.add(new_medicine)
    db.session.commit()


def update_medicine(medicine_id: int, data: dict[str, any]) -> None:

    medicine = get_medicine(medicine_id=medicine_id)

    medicine.name = data.get("name")

    db.session.commit()


def get_medicine(medicine_id: int, options: list = None) -> Medicine:

    query = Medicine.query

    if options is not None:
        query = query.options(*options)

    medicine = query.get(medicine_id)

    if medicine is None:
        raise DefaultException("medicine_not_found", code=404)

    return medicine
