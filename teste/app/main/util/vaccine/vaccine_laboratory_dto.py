from flask_restx import Namespace, fields

from app.main.service import CNPJ


class VaccineLaboratoryDTO:

    api = Namespace(
        "vaccine_laboratory", description="vaccine laboratory related operations"
    )

    vaccine_laboratory_post = api.model(
        "vaccine_laboratory_create",
        {
            "name": fields.String(
                required=True, description="vaccine laboratory name", min_length=1
            ),
            "pni_code": fields.String(
                required=True, description="Code Laboratory PNI Web Manufacturer"
            ),
            "cnpj": CNPJ(
                description="laboratory cnpj",
            ),
        },
    )

    vaccine_laboratory_put = api.clone(
        "vaccine_laboratory_put", vaccine_laboratory_post
    )

    vaccine_laboratory_response = api.clone(
        "vaccine_laboratory_response",
        vaccine_laboratory_post,
        {"id": fields.Integer(description="vaccine laboratory id")},
    )

    vaccine_laboratory_list = api.model(
        "vaccine_laboratory_list",
        {
            "current_page": fields.Integer(),
            "total_items": fields.Integer(),
            "total_pages": fields.Integer(),
            "items": fields.List(fields.Nested(vaccine_laboratory_response)),
        },
    )
