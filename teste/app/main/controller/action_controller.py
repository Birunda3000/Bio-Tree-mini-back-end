from flask import request
from flask_restx import Resource

from app.main.config import Config
from app.main.service import delete_action, get_actions, save_new_action, update_action
from app.main.util import ActionDTO, DefaultResponsesDTO

action_ns = ActionDTO.api
api = action_ns
_action_post = ActionDTO.action_post
_action_list = ActionDTO.action_list

_default_message_response = DefaultResponsesDTO.message_response
_validation_error_response = DefaultResponsesDTO.validation_error

_CONTENT_PER_PAGE = Config.CONTENT_PER_PAGE
_DEFAULT_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


@api.route("")
class Action(Resource):
    @api.doc(
        "action_list",
        params={
            "page": {"description": "Page number", "default": 1, "type": int},
            "per_page": {
                "description": "Items per page",
                "default": _DEFAULT_CONTENT_PER_PAGE,
                "enum": _CONTENT_PER_PAGE,
                "type": int,
            },
            "name": {"description": "Action name", "type": str},
        },
        description=f"List of registered actions with pagination. {_DEFAULT_CONTENT_PER_PAGE} actions per page.",
    )
    @api.marshal_with(_action_list, code=200, description="action_list")
    def get(self):
        """List all actions"""
        params = request.args
        return get_actions(params=params)

    @api.doc("create_action")
    @api.response(201, "action_created", _default_message_response)
    @api.response(400, "Input payload validation failed", _validation_error_response)
    @api.response(409, "name_in_use", _default_message_response)
    @api.expect(_action_post, validate=True)
    def post(self) -> tuple[dict[str, str], int]:
        """Creates an action"""
        data = request.json
        save_new_action(data=data)
        return {"message": "action_created"}, 201


@api.route("/<int:action_id>")
class ActionById(Resource):
    @api.doc("update_action")
    @api.response(200, "action_updated", _default_message_response)
    @api.response(400, "Input payload validation failed", _validation_error_response)
    @api.response(404, "action_not_found", _default_message_response)
    @api.response(409, "name_in_use", _default_message_response)
    @api.expect(_action_post, validate=True)
    def put(self, action_id):
        """Updates an action"""
        data = request.json
        update_action(action_id=action_id, data=data)
        return {"message": "action_updated"}, 200

    @api.doc("delete_action")
    @api.response(200, "action_deleted", _default_message_response)
    @api.response(404, "action_not_found", _default_message_response)
    @api.response(
        409, "action_is_associated_with_prescription", _default_message_response
    )
    def delete(self, action_id):
        """Deletes an action"""
        delete_action(action_id=action_id)
        return {"message": "action_deleted"}, 200
