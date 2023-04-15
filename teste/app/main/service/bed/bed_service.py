from math import ceil

from werkzeug.datastructures import ImmutableMultiDict

from app.main import db
from app.main.config import Config
from app.main.exceptions import DefaultException
from app.main.model import Bed, Room

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def get_beds(params: ImmutableMultiDict):

    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)
    bed_number = params.get("bed_number", type=int)
    available = params.get("available", type=str)
    status = params.get("status", type=str)
    room_id = params.get("room_id", type=int)

    filters = []

    if bed_number:
        filters.append(Bed.bed_number == bed_number)
    if available:
        filters.append(Bed.available == bool(eval(available.title())))
    if status:
        filters.append(Bed.status == bool(eval(status.title())))
    if room_id:
        filters.append(Bed.room_id == room_id)

    pagination = (
        Bed.query.filter(*filters)
        .order_by(Bed.id)
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return {
        "current_page": page,
        "total_items": pagination.total,
        "total_pages": ceil(pagination.total / per_page),
        "items": pagination.items,
    }


def save_new_bed(data: dict[str, any]):

    get_room(room_id=data.get("room_id"))

    new_bed = Bed(status=data.get("status"), room_id=data.get("room_id"))

    db.session.add(new_bed)
    db.session.commit()


def update_bed(bed_id: int, data: dict[str, any]):

    bed = get_bed(bed_id=bed_id)

    bed.status = data.get("status")

    db.session.commit()


def update_bed_available_field(bed_id: int, available: bool):

    bed = get_bed(bed_id=bed_id, available_check=False)

    if available == bed.available:
        if available:
            raise DefaultException("bed_already_available", code=409)
        raise DefaultException("bed_already_unavailable", code=409)

    bed.available = available


def create_hospital_first_beds(number_of_beds: int, room: Room):
    for bed_number in range(1, number_of_beds + 1):
        new_bed = Bed(bed_number=bed_number, room=room)
        db.session.add(new_bed)


def get_bed(bed_id: int, options: list = None, available_check: bool = True) -> Bed:

    query = Bed.query

    if options is not None:
        query = query.options(*options)

    bed = query.get(bed_id)

    if bed is None:
        raise DefaultException("bed_not_found", code=404)

    if available_check and not bed.available:
        raise DefaultException(message="bed_not_available", code=409)

    return bed


from app.main.service.room_service import get_room
