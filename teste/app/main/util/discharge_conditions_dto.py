from flask_restx import Namespace, fields


class DischargeConditionsDTO:
    api = Namespace(
        "discharge_conditions", description="discharge conditions related operations"
    )

    discharge_conditions_post = api.model(
        "discharge conditions create",
        {
            "name": fields.String(
                required=True, name="discharge conditions name", min_length=1
            )
        },
    )

    discharge_conditions_response = api.clone(
        "discharge conditions response",
        discharge_conditions_post,
        {"id": fields.Integer(description="discharge conditions id")},
    )

    discharge_conditions_list = api.model(
        "discharge conditions list",
        {
            "current_page": fields.Integer(description="current page"),
            "total_items": fields.Integer(description="total items"),
            "total_pages": fields.Integer(description="total pages"),
            "items": fields.List(fields.Nested(discharge_conditions_response)),
        },
    )
