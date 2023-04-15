from flask_restx import Namespace, fields

from app.main.service import CustomDate


class EnablementDTO:
    api = Namespace("enablement", description="enablement related operations")

    enablement_post = api.model(
        "enablement_post",
        {
            "code": fields.String(
                required=True,
                description="enablement code",
            ),
            "name": fields.String(
                required=True,
                description="enablement name",
                min_length=1,
            ),
            "number_of_beds": fields.Integer(
                description="enablement number of beds",
            ),
            "ordinance_number": fields.Integer(
                description="enablement ordinance number",
            ),
            "release_date": CustomDate(
                description="enablement release date",
            ),
        },
    )

    enablement_response = api.clone(
        "enablement_response",
        {"id": fields.Integer(description="enablement id")},
        enablement_post,
    )

    enablements_list = api.model(
        "enablement_list",
        {
            "current_page": fields.Integer(),
            "total_items": fields.Integer(),
            "total_pages": fields.Integer(),
            "items": fields.List(fields.Nested(enablement_response)),
        },
    )
