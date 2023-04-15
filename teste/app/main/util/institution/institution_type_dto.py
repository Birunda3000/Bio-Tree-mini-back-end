from flask_restx import Namespace, fields

from app.main.util.institution.institution_subtype_dto import InstitutionSubtypeDTO

_institution_subtype = InstitutionSubtypeDTO.institution_subtype_response


class InstitutionTypeDTO:
    api = Namespace("institution", description="institution related operations")

    institution_type_post = api.model(
        "institution type post",
        {
            "name": fields.String(
                required=True, description="institution type name", min_length=1
            )
        },
    )

    institution_type_update = api.clone("institution type put", institution_type_post)

    institution_type_response = api.clone(
        "institution type response",
        institution_type_post,
        {
            "id": fields.Integer(description="institution type id"),
            "institution_subtypes": fields.List(fields.Nested(_institution_subtype)),
        },
    )

    institution_types_list = api.model(
        "institution_types_list",
        {
            "current_page": fields.Integer(),
            "total_items": fields.Integer(),
            "total_pages": fields.Integer(),
            "items": fields.List(fields.Nested(institution_type_response)),
        },
    )
