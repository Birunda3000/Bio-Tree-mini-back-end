from flask import request
from flask_restx import Resource

from app.main.service import activate_user, activation_check_token, resend_token
from app.main.util import ActivationDTO, DefaultResponsesDTO

activation_ns = ActivationDTO.api
api = activation_ns
activation_post = ActivationDTO.activation_post

_default_message_response = DefaultResponsesDTO.message_response


@api.route("/<string:token>")
class Activation(Resource):
    @api.doc("Check token")
    @api.response(200, "token_valid", _default_message_response)
    @api.response(401, "token_expired", _default_message_response)
    @api.response(409, "token_invalid", _default_message_response)
    def get(self, token: str) -> tuple[dict[str, str], int]:
        """Check token"""
        activation_check_token(token)
        return {"message": "token_valid"}, 200

    @api.doc("Activate user")
    @api.response(201, "user_activated", _default_message_response)
    @api.response(400, "Input payload validation failed", _default_message_response)
    @api.response(401, "token_expired", _default_message_response)
    @api.response(409, "token_invalid", _default_message_response)
    @api.response(
        409,
        "user_already_activated\nuser_is_blocked\npasswords_not_match\npassword_already_created",
        _default_message_response,
    )
    @api.expect(activation_post, validate=True)
    def post(self, token: str) -> tuple[dict[str, str], int]:
        """Activate user"""
        data = request.json
        activate_user(token, data=data)
        return {"message": "user_activated"}, 201


@api.route("/resend/<int:user_id>")
class Resend(Resource):
    @api.doc("Resend token")
    @api.response(200, "activation_email_resent", _default_message_response)
    @api.response(
        404, "user_not_found\nprofessional_not_found", _default_message_response
    )
    @api.response(
        409, "user_already_activated\nuser_is_blocked", _default_message_response
    )
    def put(self, user_id: int) -> tuple[dict[str, str], int]:
        """Resend user token"""
        resend_token(user_id)
        return {"message": "activation_email_resent"}, 200
