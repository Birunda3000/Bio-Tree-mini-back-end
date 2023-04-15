from math import ceil

from werkzeug.datastructures import ImmutableMultiDict

from app.main import db
from app.main.config import Config
from app.main.exceptions import DefaultException
from app.main.model import ItemGroup

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def get_item_groups(params: ImmutableMultiDict):

    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)
    name = params.get("name", type=str)

    filters = []

    if name:
        filters.append(ItemGroup.name.ilike(f"%{name.upper()}%"))

    pagination = (
        ItemGroup.query.filter(*filters)
        .order_by(ItemGroup.id)
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return {
        "current_page": page,
        "total_items": pagination.total,
        "total_pages": ceil(pagination.total / per_page),
        "items": pagination.items,
    }


def save_new_item_group(data: dict[str, any]) -> None:

    name = data.get("name")

    if _item_group_exists(name):
        raise DefaultException("name_in_use", code=409)

    new_item_group = ItemGroup(name=name)

    db.session.add(new_item_group)
    db.session.commit()


def update_item_group(item_group_id: int, data: dict[str, str]) -> None:

    item_group = get_item_group(item_group_id=item_group_id)

    new_name = data.get("name").upper()

    if item_group.name != new_name:

        if _item_group_exists(new_name):
            raise DefaultException("name_in_use", code=409)

        item_group.name = new_name

        db.session.commit()


def delete_item_group(item_group_id: int):

    item_group = get_item_group(item_group_id=item_group_id)

    db.session.delete(item_group)
    db.session.commit()


def get_item_group(item_group_id: int, options: list = None) -> ItemGroup:

    query = ItemGroup.query

    if options is not None:
        query = query.options(*options)

    item_group = query.get(item_group_id)

    if item_group is None:
        raise DefaultException("item_group_not_found", code=404)

    return item_group


def _item_group_exists(item_group_name: str) -> bool:
    return (
        ItemGroup.query.with_entities(ItemGroup.id)
        .filter(ItemGroup.name == item_group_name.upper())
        .scalar()
        is not None
    )
