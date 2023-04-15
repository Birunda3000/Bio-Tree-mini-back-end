from flask import request
from flask_restx import Resource

from app.main.config import Config
from app.main.service import (
    delete_attendance_room,
    get_attendance_room_by_id,
    get_attendance_rooms,
    save_new_attendance_room,
    update_attendance_room,
)
from app.main.util import AttendanceRoomDTO, DefaultResponsesDTO

attendance_room_ns = AttendanceRoomDTO.api
api = attendance_room_ns

_attendance_room_post = AttendanceRoomDTO.attendance_room_post

_attendance_room_list = AttendanceRoomDTO.attendance_room_list

_attendance_room_response = AttendanceRoomDTO.attendance_room_response

_default_message_response = DefaultResponsesDTO.message_response

_CONTENT_PER_PAGE = Config.CONTENT_PER_PAGE
_DEFAULT_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


@api.route("")
class AttendanceRoom(Resource):
    @api.doc(
        "list a attendance room",
        params={
            "page": {"description": "Page number", "default": 1, "type": int},
            "per_page": {
                "description": "Items per page",
                "default": _DEFAULT_CONTENT_PER_PAGE,
                "enum": _CONTENT_PER_PAGE,
                "type": int,
            },
            "acronym": {
                "description": "Attendance room acronym",
                "type": str,
            },
            "description": {
                "description": "Attendance room description",
                "type": str,
            },
        },
        description=f"List of registered attendance rooms with pagination. {_DEFAULT_CONTENT_PER_PAGE} attendance rooms per page.",
    )
    @api.marshal_with(
        _attendance_room_list, code=200, description="attendance_room_list"
    )
    def get(self):
        """List registered attendance rooms with pagination"""
        params = request.args
        return get_attendance_rooms(params=params)

    @api.doc("create_a_attendance_room")
    @api.expect(_attendance_room_post, validate=True)
    @api.response(201, "attendance_room_created", _default_message_response)
    @api.response(400, "invalid_payload", _default_message_response)
    @api.response(409, "acronym_in_use\ndescription_in_use", _default_message_response)
    def post(self):
        """Create a new attendance room"""
        data = request.json
        save_new_attendance_room(data=data)
        return {"message": "attendance_room_created"}, 201


@api.route("/<int:attendance_room_id>")
class AttendanceRoomById(Resource):
    @api.doc("get a attendance room")
    @api.marshal_with(
        _attendance_room_response, code=200, description="attendance_room"
    )
    @api.response(200, "attendance_room", _attendance_room_response)
    def get(self, attendance_room_id):
        """Get a attendance room"""
        return get_attendance_room_by_id(attendance_room_id=attendance_room_id)

    @api.doc("update a attendance room")
    @api.expect(_attendance_room_post, validate=True)
    @api.response(200, "attendance_room_updated", _default_message_response)
    @api.response(400, "invalid_payload", _default_message_response)
    @api.response(409, "acronym_in_use\ndescription_in_use", _default_message_response)
    def put(self, attendance_room_id):
        """Update a attendance room"""
        data = request.json
        update_attendance_room(attendance_room_id=attendance_room_id, data=data)
        return {"message": "attendance_room_updated"}

    @api.doc("delete a attendance room")
    @api.response(200, "attendance_room_deleted", _default_message_response)
    def delete(self, attendance_room_id):
        """Delete a attendance room"""
        delete_attendance_room(attendance_room_id=attendance_room_id)
        return {"message": "attendance_room_deleted"}
