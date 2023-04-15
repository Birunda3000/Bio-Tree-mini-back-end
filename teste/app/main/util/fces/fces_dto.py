from flask_restx import Namespace, fields

from app.main.model import PAYMENT_TO_PROVIDER_TYPE, PERSON_TYPE, SITUATION_TYPE
from app.main.service import CNPJ, CPF, Email
from app.main.util.company_address_dto import CompanyAddressDTO
from app.main.util.contact_dto import ContactDTO

_company_address = CompanyAddressDTO.company_address
_contact = ContactDTO.contact


class FcesDTO:
    api = Namespace("fces", description="fces related operations")

    fces_id = {"id": fields.Integer(required=True, description="fces id", example=1)}

    fces_corporate_name = {
        "corporate_name": fields.String(
            required=True, description="fces corporate name", min_length=1
        )
    }

    fces_post = api.model(
        "fces_post",
        {
            "maintainer_id": fields.Integer(
                required=True, description="maintainer relationship", example=1
            ),
            "professional_id": fields.Integer(
                required=True, description="professional relationship", example=1
            ),
            "corporate_name": fields.String(
                required=True,
                description="fces corporate name",
            ),
            "commercial_name": fields.String(
                required=True,
                description="fces commercial name",
            ),
            "cnes_code": fields.Integer(
                required=True, description="fces cnes code", example=12345
            ),
            "person_type": fields.String(
                required=True, description="fces person type", enum=PERSON_TYPE
            ),
            "cnpj": CNPJ(
                description="fces cnpj",
            ),
            "cpf": CPF(
                description="fces cpf",
            ),
            "email": Email(required=True, description="fces mail"),
            "establishment_code": fields.Integer(
                required=True, description="fces establishment code", example=12345
            ),
            "situation": fields.String(
                required=True, description="fces situation", enum=SITUATION_TYPE
            ),
            "establishment_type": fields.String(
                required=True,
                description="fces establishment type",
            ),
            "establishment_subtype": fields.String(
                required=True,
                description="fces establishment type",
            ),
            "regulatory_registration_end_date": fields.String(
                required=True, description="fces regulatory registration end date"
            ),
            "payment_to_provider": fields.String(
                required=True,
                description="fces payment to provider",
                enum=PAYMENT_TO_PROVIDER_TYPE,
            ),
            "company_address": fields.Nested(_company_address),
            "contact": fields.Nested(_contact),
        },
    )

    fces_put = api.model(
        "fces_put",
        {
            "maintainer_id": fields.Integer(
                required=True, description="maintainer relationship", example=1
            ),
            "professional_id": fields.Integer(
                required=True, description="professional relationship", example=1
            ),
            "corporate_name": fields.String(
                required=True,
                description="fces corporate name",
            ),
            "commercial_name": fields.String(
                required=True,
                description="fces commercial name",
            ),
            "email": Email(required=True, description="fces mail"),
            "establishment_code": fields.Integer(
                required=True, description="fces establishment code", example=12345
            ),
            "situation": fields.String(
                required=True, description="fces situation", enum=SITUATION_TYPE
            ),
            "establishment_type": fields.String(
                required=True,
                description="fces establishment type",
            ),
            "establishment_subtype": fields.String(
                required=True,
                description="fces establishment type",
            ),
            "regulatory_registration_end_date": fields.String(
                required=True, description="fces regulatory registration end date"
            ),
            "payment_to_provider": fields.String(
                required=True,
                description="fces payment to provider",
                enum=PAYMENT_TO_PROVIDER_TYPE,
            ),
            "company_address": fields.Nested(_company_address),
            "contact": fields.Nested(_contact),
        },
    )

    fces_response = api.clone(
        "fces_response",
        fces_post,
        {"id": fields.Integer(description="fces id")},
    )

    fces_list = api.model(
        "fces_list",
        {
            "current_page": fields.Integer(),
            "total_items": fields.Integer(),
            "total_pages": fields.Integer(),
            "items": fields.List(fields.Nested(fces_response)),
        },
    )
