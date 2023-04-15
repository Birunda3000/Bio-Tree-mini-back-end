from flask_restx import Namespace, fields


class MedicalSpecialtyDTO:
    api = Namespace(
        "medical_specialty", description="medical specialty related operations"
    )

    medical_specialty_post = api.model(
        "medical specialty post",
        {
            "name": fields.String(
                required=True, description="medical specialty name", min_length=1
            )
        },
    )

    medical_specialty_update = api.clone(
        "medical specialty put", medical_specialty_post
    )

    medical_specialty_response = api.clone(
        "medical specialty response",
        medical_specialty_post,
        {"id": fields.Integer(description="medical specialty id")},
    )

    medical_specialties_list = api.model(
        "medical specialty list",
        {
            "current_page": fields.Integer(),
            "total_items": fields.Integer(),
            "total_pages": fields.Integer(),
            "items": fields.List(fields.Nested(medical_specialty_response)),
        },
    )
