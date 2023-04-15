from flask_restx import Namespace, fields



class AttendanceRoomDTO:
    api = Namespace("attendance_room", description="attendance room related operations")

    attendance_room_post = api.model(
        "attendance room create",
        {
            "call_panel_id": fields.Integer(required=True, description="call panel relationship"),
            "acronym": fields.String(required=True, description="attendance room acronym"),
            "description": fields.String(required=True, description="attendance room description"),
        },
    )

    attendance_room_response = api.clone(
        "attendance room response",
        attendance_room_post,
        {"id": fields.Integer(description="attendance room id")},
    )

    attendance_room_list = api.model(
        "attendance room list",
        {
            "current_page": fields.Integer(description="current page"),
            "total_items": fields.Integer(description="total items"),
            "total_pages": fields.Integer(description="total pages"),
            "items": fields.List(fields.Nested(attendance_room_response)),
        },
    )