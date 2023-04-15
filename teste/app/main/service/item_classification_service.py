from math import ceil

from werkzeug.datastructures import ImmutableMultiDict

from app.main import db
from app.main.config import Config
from app.main.exceptions import DefaultException
from app.main.model import ItemClassification

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def get_item_classifications(params: ImmutableMultiDict):

    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)
    name = params.get("name", type=str)

    filters = []

    if name:
        filters.append(ItemClassification.name.ilike(f"%{name.upper()}%"))

    pagination = (
        ItemClassification.query.filter(*filters)
        .order_by(ItemClassification.id)
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return {
        "current_page": page,
        "total_items": pagination.total,
        "total_pages": ceil(pagination.total / per_page),
        "items": pagination.items,
    }


def save_new_item_classification(data: dict[str, any]) -> None:

    name = data.get("name")

    if _item_classification_exists(name):
        raise DefaultException("name_in_use", code=409)

    new_item_classification = ItemClassification(name=name)

    db.session.add(new_item_classification)
    db.session.commit()


def update_item_classification(
    item_classification_id: int, data: dict[str, str]
) -> None:

    item_classification = get_item_classification(
        item_classification_id=item_classification_id
    )

    new_name = data.get("name").upper()

    if item_classification.name != new_name and _item_classification_exists(new_name):
        raise DefaultException("name_in_use", code=409)

    item_classification.name = new_name

    db.session.commit()


def delete_item_classification(item_classification_id: int):

    item_classification = get_item_classification(
        item_classification_id=item_classification_id
    )

    db.session.delete(item_classification)
    db.session.commit()


def get_item_classification(
    item_classification_id: int, options: list = None
) -> ItemClassification:

    query = ItemClassification.query

    if options is not None:
        query = query.options(*options)

    item_classification = query.get(item_classification_id)

    if item_classification is None:
        raise DefaultException("item_classification_not_found", code=404)

    return item_classification


def _item_classification_exists(item_classification_name: str) -> bool:
    return (
        ItemClassification.query.with_entities(ItemClassification.id)
        .filter(ItemClassification.name == item_classification_name.upper())
        .scalar()
        is not None
    )
