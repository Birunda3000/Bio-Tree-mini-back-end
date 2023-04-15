from flask_restx import Namespace, fields

from app.main.util.action_dto import ActionDTO
from app.main.util.protocol_dto import ProtocolDTO

_action_response = ActionDTO.action_response
_protocol_response = ProtocolDTO.protocol_response


class PrescriptionDTO:
    api = Namespace("prescription", description="prescription related operations")

    prescription_post = api.model(
        "prescription",
        {
            "protocol_id": fields.Integer(required=True, description="protocol id"),
            "actions_ids": fields.List(
                fields.Integer(description="action id"),
                required=True,
                description="action id list",
            ),
        },
    )

    prescription_response = api.model(
        "prescription_response",
        {
            "id": fields.Integer(description="prescription id"),
            "protocol": fields.Nested(
                _protocol_response, description="protocol relationship"
            ),
            "actions": fields.List(
                fields.Nested(_action_response), description="actions relationship"
            ),
        },
    )

    prescription_list = api.model(
        "prescription_list",
        {
            "current_page": fields.Integer(),
            "total_items": fields.Integer(),
            "total_pages": fields.Integer(),
            "items": fields.List(fields.Nested(prescription_response)),
        },
    )
