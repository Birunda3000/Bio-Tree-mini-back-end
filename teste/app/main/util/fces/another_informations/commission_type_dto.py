from flask_restx import Namespace, fields


class CommissionTypeDTO:
    api = Namespace("commission_type", description="commission type related operations")

    commission_type_response = api.model(
        "commission_type_response",
        {
            "id": fields.Integer(description="commission type id"),
            "name": fields.String(description="commission type name"),
        },
    )

    commission_type_id_response = api.model(
        "commission_type_id_response",
        {
            "id": fields.Integer(description="commission type id"),
        },
    )
