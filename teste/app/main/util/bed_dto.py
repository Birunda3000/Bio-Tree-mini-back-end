from flask_restx import Namespace, fields

from app.main.util.room_dto import RoomDTO

_room_id = RoomDTO.room_id


class BedDTO:
    api = Namespace("bed", description="bed related operations")

    bed_id_room = api.model(
        "bed_id_room",
        {"id": fields.Integer(description="bed id"), "room": fields.Nested(_room_id)},
    )

    bed_response = api.model(
        "bed_response",
        {
            "id": fields.Integer(description="bed id"),
            "bed_number": fields.Integer(description="bed number"),
            "available": fields.Boolean(description="bed occupation"),
            "status": fields.Boolean(description="bed status"),
            "room_id": fields.Integer(description="room id"),
        },
    )

    bed_list = api.model(
        "bed_list",
        {
            "current_page": fields.Integer(),
            "total_items": fields.Integer(),
            "total_pages": fields.Integer(),
            "items": fields.List(fields.Nested(bed_response)),
        },
    )

    bed_update = api.model(
        "bed_update",
        {
            "status": fields.Boolean(
                required=True,
                description="false if bed is unable to be used for some reason",
            ),
        },
    )

    bed_create = api.clone(
        "bed_create",
        bed_update,
        {"room_id": fields.Integer(required=True, description="room id")},
    )
