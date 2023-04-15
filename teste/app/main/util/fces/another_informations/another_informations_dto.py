from flask_restx import Namespace, fields

from app.main.model import (
    COVENANT,
    ISSUING_AGENCY,
    NATURE_ORGANIZATION,
    SERVICE_SHIFT,
    TAX_WITHHOLDING,
)
from app.main.service import CustomDatePast
from app.main.util.fces.another_informations.commission_type_dto import (
    CommissionTypeDTO,
)
from app.main.util.fces.another_informations.leavings_dto import LeavingsDTO

_commission_type_response = CommissionTypeDTO.commission_type_response
_commission_type_id_response = CommissionTypeDTO.commission_type_id_response
_leavings_response = LeavingsDTO.leavings_response
_leavings_id_response = LeavingsDTO.leavings_id_response


class AnotherInformationsDTO:
    api = Namespace(
        "another_informations", description="another informations related operations"
    )

    another_informations_base = api.model(
        "another_informations_base",
        {
            "sanitary_number": fields.String(
                description="sanitary permit number ", required=True
            ),
            "issuance_date": CustomDatePast(
                required=True,
                description="sanitary permit issuance date",
            ),
            "issuing_agency": fields.String(
                description="sanitary permit issuing agency enumerate",
                required=True,
                enum=ISSUING_AGENCY,
            ),
            "bank": fields.String(
                description="bank code",
                required=True,
                min_length=3,
                max_length=3,
                example="001",
                pattern="^[0-9]+$",
            ),
            "agency": fields.String(description="bank agency code", required=True),
            "current_account": fields.String(
                description="current account number", required=True
            ),
            "administrative_field": fields.String(
                description="administrative field", required=True, example="Federal"
            ),
            "hierarchy_level": fields.String(
                description="hierarchy level", required=True
            ),
            "teaching_research_activity_text": fields.String(
                description="teching research activity text"
            ),
            "tax_withholding": fields.String(
                description="tax withholding enumerate",
                enum=TAX_WITHHOLDING,
                required=True,
            ),
            "service_shift": fields.String(
                description="service shift enumerate", enum=SERVICE_SHIFT, required=True
            ),
            "nature_organization": fields.String(
                description="service shift enumerate",
                enum=NATURE_ORGANIZATION,
                required=True,
            ),
            "attendance": fields.String(description="attendance", required=True),
            "covenant": fields.String(
                description="covenant enumerate", enum=COVENANT, required=True
            ),
        },
    )

    another_informations_get = api.clone(
        "another_informations_get",
        another_informations_base,
        {
            "leavings_selected": fields.List(
                fields.Nested(_leavings_id_response),
                description="a list with selected leavings",
            ),
            "commission_types_selected": fields.List(
                fields.Nested(_commission_type_id_response),
                description="a list with selected commission types",
            ),
        },
    )

    another_informations_post = api.clone(
        "another_informations_post",
        another_informations_base,
        {
            "leavings_selected": fields.List(
                fields.Integer(description="leaving id"),
                description="a list with selected leavings",
                example=[1, 2],
                min_items=1,
            ),
            "commission_types_selected": fields.List(
                fields.Integer(description="commission_type id"),
                description="a list with selected commission types",
                example=[2, 5, 9],
            ),
        },
    )

    another_informations_put = api.clone(
        "another_informations_put", another_informations_post
    )

    another_informations_response = api.clone(
        "another_informations_response",
        another_informations_get,
        {
            "leavings": fields.List(fields.Nested(_leavings_response)),
            "commission_types": fields.List(fields.Nested(_commission_type_response)),
            "id": fields.Integer(description="another informations id"),
        },
    )
