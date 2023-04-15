from flask_restx import Namespace, fields
from werkzeug.datastructures import FileStorage


class ClassificationDTO:
    api = Namespace("classification", description="classification related operations")

    upload_parser = api.parser()

    upload_parser.add_argument(
        "file", location="files", type=FileStorage, required=True
    )

    classification_post = api.model(
        "classification post",
        {
            "service_id": fields.Integer(
                required=True, description="service relationship", example=1
            ),
            "code": fields.String(
                required=True,
                description="classification code",
                min_length=3,
                max_length=3,
                example="150",
                pattern="^[0-9]+$",
            ),
            "name": fields.String(
                required=True,
                description="classification name",
                min_length=1,
            ),
        },
    )

    classification_update = api.clone("classification put", classification_post)

    classification_response = api.clone(
        "classification response",
        {"id": fields.Integer(description="classification id")},
        classification_post,
    )

    classification_list = api.model(
        "classification_list",
        {
            "current_page": fields.Integer(),
            "total_items": fields.Integer(),
            "total_pages": fields.Integer(),
            "items": fields.List(fields.Nested(classification_response)),
        },
    )
