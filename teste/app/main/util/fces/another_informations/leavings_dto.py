from flask_restx import Namespace, fields


class LeavingsDTO:
    api = Namespace("leavings", description="leavings related operations")

    leavings_response = api.model(
        "leavings_response",
        {
            "id": fields.Integer(description="leavings id"),
            "name": fields.String(description="leavings name"),
        },
    )

    leavings_id_response = api.model(
        "leavings_id_response",
        {
            "id": fields.Integer(description="leavings id"),
        },
    )
