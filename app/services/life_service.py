from models import Life
from config import db, Config

from math import ceil

from sqlalchemy.orm import joinedload
from werkzeug.datastructures import ImmutableMultiDict
from responses import *

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE

def get_all_lives(params: ImmutableMultiDict):
    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)
    title = params.get("title", type=str)
    description = params.get("description", type=str)
    content = params.get("content", type=str)
    tags = params.get("tags", type=str)

    filters = []

    if title:
        filters.append(Life.title.ilike(f"%{title}%"))
    if description:
        filters.append(Life.description.ilike(f"%{description}%"))
    if content:
        filters.append(Life.content.ilike(f"%{content}%"))
    if tags:
        filters.append(Life.tags.ilike(f"%{tags}%"))
    
    pagination = (
        Life.query.filter(*filters)
        .order_by(Life.id)
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return {
        "current_page": page,
        "total_items": pagination.total,
        "total_pages": ceil(pagination.total / per_page),
        "items": pagination.items,
    }

def save_new_life(data):
    life = Life.query.filter_by(title=data["title"]).first()
    if not life:
        new_life = Life(
            title=data.get("title"),
            description=data.get("description"),
            content=data.get("content"),
            tags=data.get("tags"),
        )
        
        db.session.add(new_life)
        db.session.commit()
        
        response_object = {
            "status": "success",
            "message": "Life successfully created.",
        }
        return response_object, 201
    else:
        response_object = {
            "status": "fail",
            "message": "This Life already exists.",
        }
        return response_object, 409

