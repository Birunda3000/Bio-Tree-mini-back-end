from flask_restx import Namespace, fields


class SanitaryDistrictDTO:

    api = Namespace(
        "sanitary_district", description="sanitary district related operations"
    )

    sanitary_district_post = api.model(
        "sanitary_district_post",
        {
            "name": fields.String(
                required=True, description="sanitary district name", min_length=1
            ),
        },
    )

    sanitary_district_put = api.clone("sanitary_district_put", sanitary_district_post)

    sanitary_district_response = api.model(
        "sanitary_district_response",
        {
            "id": fields.Integer(description="sanitary district id"),
            "name": fields.String(description="sanitary district name"),
        },
    )

    sanitary_district_list = api.model(
        "sanitary_district_list",
        {
            "current_page": fields.Integer(),
            "total_items": fields.Integer(),
            "total_pages": fields.Integer(),
            "items": fields.List(fields.Nested(sanitary_district_response)),
        },
    )
