import math

from sqlalchemy import or_

from app.main import db
from app.main.config import Config
from app.main.exceptions import DefaultException
from app.main.model import AttendanceRoom
from app.main.model import CallPanel
from .call_panel_service import get_call_panel

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def get_attendance_rooms(params: dict[str, any]):
    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)
    acronym = params.get("acronym", type=str)
    description = params.get("description", type=str)

    filters = []

    if acronym:
        filters.append(AttendanceRoom.acronym.ilike(f"%{acronym}%"))
    if description:
        filters.append(AttendanceRoom.description.ilike(f"%{description}%"))

    pagination = (
        AttendanceRoom.query.filter(*filters)
        .order_by(AttendanceRoom.id)
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return {
        "current_page": page,
        "total_itens": pagination.total,
        "total_pages": math.ceil(pagination.total / per_page),
        "items": pagination.items,
    }


def get_attendance_room_by_id(attendance_room_id: int) -> AttendanceRoom:
    return get_attendance_room(attendance_room_id=attendance_room_id)


def save_new_attendance_room(data: dict[str, any]):

    if (
        attendance_room := AttendanceRoom.query.with_entities(
            AttendanceRoom.acronym,
            AttendanceRoom.description,
        )
        .filter(
            or_(
                AttendanceRoom.acronym == data.get("acronym"),
                AttendanceRoom.description == data.get("description"),
            )
        )
        .first()
    ):
        if attendance_room.acronym == data.get("acronym"):
            raise DefaultException("acronym_in_use", code=409)
        elif attendance_room.description == data.get("description"):
            raise DefaultException("description_in_use", code=409)

    call_panel = get_call_panel(data.get("call_panel_id"))
    new_attendance_room = AttendanceRoom(
        acronym = data.get("acronym"),
        description = data.get("description"),
        call_panel = call_panel
    )

    db.session.add(new_attendance_room)
    db.session.commit()


def update_attendance_room(attendance_room_id: int, data: dict[str, any]):
    filters = [
        or_(
            AttendanceRoom.acronym == data.get("acronym"),
            AttendanceRoom.description == data.get("description")
        )
    ]
    attendance_room_search = AttendanceRoom.query.filter(*filters).first()
    if attendance_room_search and attendance_room_search.id != attendance_room_id:
        if attendance_room_search.acronym == data.get("acronym"):
            raise DefaultException("acronym_in_use", code=409)
        elif attendance_room_search.description == data.get("description"):
            raise DefaultException("description_in_use", code=409)

    call_panel = get_call_panel(data.get("call_panel_id"))
    attendance_room = get_attendance_room(attendance_room_id)
    attendance_room.acronym = data.get("acronym")
    attendance_room.description = data.get("description")
    attendance_room.call_panel = call_panel

    db.session.commit()


def delete_attendance_room(attendance_room_id: int):
    attendance_room = get_attendance_room(attendance_room_id)

    db.session.delete(attendance_room)
    db.session.commit()


def get_attendance_room(
    attendance_room_id: int, options: list = None
) -> AttendanceRoom:

    query = AttendanceRoom.query

    if options is not None:
        query = query.options(*options)

    attendance_room = query.get(attendance_room_id)

    if attendance_room is None:
        raise DefaultException("attendance_room_not_found", code=404)

    return attendance_room
