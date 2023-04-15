from flask_restx import Namespace, fields


class Cid10DTO:
    api = Namespace("cid_10", description="cid 10 related operations")

    cid_10_response = api.model(
        "cid_10_response",
        {
            "id": fields.Integer(description="cid 10 id"),
            "code": fields.String(description="cid 10 identifier"),
            "category": fields.Integer(description="cid 10 category"),
        },
    )
