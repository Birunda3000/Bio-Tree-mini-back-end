from math import ceil

from config import Config, db
from models import Tag
from responses import DefaultException, response
from werkzeug.datastructures import ImmutableMultiDict

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def get_tags(params: ImmutableMultiDict) -> dict[str, any]:
    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)
    name = params.get("name", type=str)
    description = params.get("description", type=str)
    filters = []
    if name:
        filters.append(Tag.name.ilike(f"%{name}%"))
    if description:
        filters.append(Tag.description.ilike(f"%{description}%"))
    pagination = (
        Tag.query.filter(*filters)
        .order_by(Tag.id)
        .paginate(page=page, per_page=per_page, error_out=False)
    )
    return {
        "current_page": page,
        "total_items": pagination.total,
        "total_pages": ceil(pagination.total / per_page),
        "items": pagination.items,
    }


def get_tag(tag_id: int, options: list = None) -> Tag:
    """Get a tag"""
    if options is None:
        options = []
    tag = Tag.query.options(*options).filter_by(id=tag_id).first()
    if tag is None:
        raise DefaultException(message="Tag_not_found", code=404)
    return tag


def save_new_tag(data: dict[str, any]) -> dict[str, any]:
    tag = Tag.query.filter_by(name=data["name"]).first()

    if tag is not None:
        raise DefaultException(message="This_Tag_already_exists", code=409)

    new_tag = Tag(
        name=data.get("name"),
        description=data.get("description"),
    )
    db.session.add(new_tag)
    db.session.commit()
    return response(status="success", message="Tag_successfully_created", code=201)


def update_tag_by_id(tag_id, data) -> dict[str, any]:
    updated_tag = get_tag(tag_id)
    print(updated_tag)
    if data.get("name") != updated_tag.name:  # Means that the name is being updated
        tag = Tag.query.filter_by(name=data.get("name")).first()
        if tag is not None:  # Means that the new name already exists
            raise DefaultException(message="This_Tag_already_exists", code=409)

    updated_tag.name = data.get("name")
    updated_tag.description = data.get("description")
    db.session.commit()
    return response(status="success", message="Tag_successfully_updated", code=200)


def delete_tag_by_id(tag_id):
    tag = get_tag(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return response(status="success", message="Tag_successfully_deleted", code=200)
