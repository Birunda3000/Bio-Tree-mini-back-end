from flask_restx import Namespace, fields


class RoomDTO:
    api = Namespace("room", description="room related operations")

    room_id = api.model(
        "room_id",
        {
            "id": fields.Integer(description="room id"),
        },
    )

    room_update = api.model(
        "room_update",
        {
            "name": fields.String(required=True, description="room name", min_length=1),
        },
    )

    room_create = api.model(
        "room_create",
        {
            "name": fields.String(required=True, description="room name", min_length=1),
            "number_of_beds": fields.Integer(description="number of beds", min=1),
        },
    )

    room_response = api.model(
        "room_response",
        {
            "id": fields.Integer(description="room id"),
            "name": fields.String(required=True, description="room name"),
            "total_beds": fields.Integer(description="total number of beds"),
            "total_available_beds": fields.Integer(
                required=True, description="number of available beds"
            ),
        },
    )

    room_list = api.model(
        "room_list",
        {
            "current_page": fields.Integer(),
            "total_items": fields.Integer(),
            "total_pages": fields.Integer(),
            "items": fields.List(fields.Nested(room_response)),
        },
    )
