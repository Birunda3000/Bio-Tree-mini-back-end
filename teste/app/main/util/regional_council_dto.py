from flask_restx import Namespace, fields

from app.main.service import CustomDatePast

from ..enum import *


class RegionalCouncilDTO:
    api = Namespace(
        "regional_council", description="regional council related operations"
    )

    regional_council_post = api.model(
        "regional_council_post",
        {
            "agency_id": fields.Integer(required=True, description="agency id"),
            "regional_council_number": fields.String(
                required=True, description="regional council number"
            ),
            "FU_of_council": fields.String(
                required=True,
                description="FU of council",
                enum=STATES_OPTIONS,
            ),
            "actual": fields.Boolean(required=True, description="actual"),
            "last_occurrence_of_SCNES": CustomDatePast(
                required=True, description="last occurrence of SCNES"
            ),
        },
    )

    regional_council_response = api.clone(
        "regional_council_response",
        regional_council_post,
        {"id": fields.Integer(description="regional council id")},
    )

    regional_council_list = api.model(
        "regional_council_list",
        {
            "items": fields.List(fields.Nested(regional_council_response)),
        },
    )
