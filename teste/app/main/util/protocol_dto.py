from flask_restx import Namespace, fields

from app.main.model import PROTOCOL_TYPES


class ProtocolDTO:
    api = Namespace("protocol", description="protocol related operations")

    protocol_post = api.model(
        "protocol_create",
        {
            "name": fields.String(
                required=True, description="protocol name", min_length=1
            ),
            "protocol_type": fields.String(
                required=True, description="protocol type", enum=PROTOCOL_TYPES
            ),
        },
    )

    protocol_response = api.clone(
        "protocol_response",
        protocol_post,
        {"id": fields.Integer(description="protocol id")},
    )

    protocol_response_with_no_id = api.clone(
        "protocol_response_with_no_id", protocol_post
    )

    protocol_list = api.model(
        "protocol_list",
        {
            "current_page": fields.Integer(),
            "total_items": fields.Integer(),
            "total_pages": fields.Integer(),
            "items": fields.List(fields.Nested(protocol_response)),
        },
    )
