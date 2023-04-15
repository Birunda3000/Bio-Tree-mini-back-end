from flask_restx import Namespace, fields


class InstitutionSubtypeDTO:
    api = Namespace(
        "institution_subtype", description="institution subtype related operations"
    )

    institution_subtype_post = api.model(
        "institution subtype post",
        {
            "institution_type_id": fields.Integer(
                required=True, description="institution type relationship", example=1
            ),
            "name": fields.String(
                required=True,
                description="institution subtype name",
                min_length=1,
            ),
        },
    )

    institution_subtype_update = api.clone(
        "institution subtype put", institution_subtype_post
    )

    institution_subtype_response = api.clone(
        "institution subtype response",
        institution_subtype_post,
        {"id": fields.Integer(description="institution subtype id")},
    )

    institution_subtype_list = api.model(
        "institution_subtype_list",
        {
            "current_page": fields.Integer(),
            "total_items": fields.Integer(),
            "total_pages": fields.Integer(),
            "items": fields.List(fields.Nested(institution_subtype_response)),
        },
    )
