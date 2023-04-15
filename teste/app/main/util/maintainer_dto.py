from flask_restx import Namespace, fields

from app.main.model import UNIT_TYPE
from app.main.service import CNPJ, CustomDate, Email
from app.main.util.address_dto import AddressDTO
from app.main.util.contact_dto import ContactDTO

_address = AddressDTO.address
_contact = ContactDTO.contact


class MaintainerDTO:
    api = Namespace("maintainer", description="maintainer related operations")

    maintainer_post = api.model(
        "maintainer_post",
        {
            "corporate_name": fields.String(
                required=True,
                description="maintainer corporate name",
            ),
            "commercial_name": fields.String(
                required=True,
                description="maintainer commercial name",
            ),
            "cnpj": CNPJ(
                required=True,
                description="maintainer cnpj",
            ),
            "regional_number": fields.Integer(
                required=True, description="maintainer regional number"
            ),
            "unit_type": fields.String(
                required=True, description="maintainer unit type", enum=UNIT_TYPE
            ),
            "email": Email(
                required=True,
                description="maintainer mail",
            ),
            "address": fields.Nested(_address),
            "contact": fields.Nested(_contact),
        },
    )

    maintainer_put = api.clone(
        "maintainer_put",
        maintainer_post,
    )

    maintainer_response = api.clone(
        "maintainer_response",
        maintainer_post,
        {"id": fields.Integer(description="maintainer id")},
    )

    maintainer_list = api.model(
        "maintainer_list",
        {
            "current_page": fields.Integer(),
            "total_items": fields.Integer(),
            "total_pages": fields.Integer(),
            "items": fields.List(fields.Nested(maintainer_response)),
        },
    )
