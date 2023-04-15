from flask_restx import Namespace, fields


class CooperativeDTO:
    api = Namespace("cooperative", description="cooperative related operations")

    cooperative_post = api.model(
        "cooperative_post",
        {
            "name": fields.String(
                description="cooperative name",
                min_length=1,
                required=True,
            ),
            "cbo": fields.String(
                description="cooperative cbo",
                min_length=1,
                required=True,
            ),
        },
    )

    cooperative_update = api.clone("cooperative_put", cooperative_post)

    cooperative_response = api.clone(
        "cooperative_response",
        {"id": fields.Integer(description="cooperative id")},
        cooperative_post,
    )

    cooperative_list = api.model(
        "cooperative_list",
        {
            "current_page": fields.Integer(),
            "total_items": fields.Integer(),
            "total_pages": fields.Integer(),
            "items": fields.List(fields.Nested(cooperative_response)),
        },
    )
