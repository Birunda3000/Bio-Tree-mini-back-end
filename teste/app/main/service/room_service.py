from math import ceil

from sqlalchemy import and_, case, func
from werkzeug.datastructures import ImmutableMultiDict

from app.main import db
from app.main.config import Config
from app.main.exceptions import DefaultException
from app.main.model import Bed, Room

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def get_rooms(params: ImmutableMultiDict):

    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)
    name = params.get("name", type=str)

    filters = []

    if name:
        filters.append(Room.name.ilike(f"%{name.upper()}%"))

    pagination = (
        Room.query.with_entities(
            Room.id,
            Room.name,
            func.count(Bed.id).label("total_beds"),
            func.count(
                case([(and_(Bed.available == True, Bed.status == True), Bed.id)])
            ).label("total_available_beds"),
        )
        .select_from(Room)
        .join(Bed, isouter=True)
        .filter(*filters)
        .group_by(Room.id)
        .order_by(Room.id)
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return {
        "current_page": page,
        "total_items": pagination.total,
        "total_pages": ceil(pagination.total / per_page),
        "items": pagination.items,
    }


def save_new_room(data: dict[str, any]) -> None:
    if _room_exists(data.get("name")):
        raise DefaultException("name_in_use", code=409)

    new_room = Room(name=data.get("name"))

    create_hospital_first_beds(number_of_beds=data.get("number_of_beds"), room=new_room)

    db.session.add(new_room)
    db.session.commit()


def update_room(room_id: int, data: dict[str, str]) -> None:

    room = get_room(room_id=room_id)

    new_name = data.get("name")

    if room.name != new_name and _room_exists(new_name):
        raise DefaultException("name_in_use", code=409)

    room.name = new_name
    db.session.commit()


def _room_exists(room_name: str) -> bool:
    return (
        Room.query.with_entities(Room.id)
        .filter(Room.name == room_name.upper())
        .scalar()
        is not None
    )


def get_room(room_id: int, options: list = None) -> Room:

    query = Room.query

    if options is not None:
        query = query.options(*options)

    room = query.get(room_id)

    if room is None:
        raise DefaultException("room_not_found", code=404)

    return room


from app.main.service.bed.bed_service import create_hospital_first_beds
