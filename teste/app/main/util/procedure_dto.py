from flask_restx import Namespace, fields
from werkzeug.datastructures import FileStorage


class ProcedureDTO:
    api = Namespace("procedure", description="procedure related operations")

    upload_parser = api.parser()
    upload_parser.add_argument(
        "file", location="files", type=FileStorage, required=True
    )

    procedure_description = api.model(
        "procedure_description",
        {
            "id": fields.Integer(example=1),
            "description": fields.String(),
        },
    )

    procedure = api.model(
        "procedure",
        {
            "id": fields.Integer(),
            "code": fields.String(),
            "classification": fields.String(),
            "dv": fields.Integer(),
            "description": fields.String(),
            "price": fields.Float(),
            "active": fields.Boolean(),
        },
    )

    procedures_list = api.model(
        "procedures_list",
        {
            "current_page": fields.Integer(),
            "total_items": fields.Integer(),
            "total_pages": fields.Integer(),
            "items": fields.List(fields.Nested(procedure)),
        },
    )
