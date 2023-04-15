from flask_restx import Namespace, fields

from .classification_dto import ClassificationDTO

_classification = ClassificationDTO.classification_response


class ServiceDTO:
    api = Namespace("service", description="service related operations")

    service_post = api.model(
        "service_post",
        {
            "code": fields.String(
                required=True,
                description="service code",
                min_length=3,
                max_length=3,
                example="150",
                pattern="^[0-9]+$",
            ),
            "name": fields.String(
                required=True, description="service name", min_length=1
            ),
        },
    )

    service_update = api.clone("service put", service_post)

    service_response = api.clone(
        "service_response",
        service_post,
        {
            "id": fields.Integer(description="service id"),
            "classifications": fields.List(fields.Nested(_classification)),
        },
    )

    service_list = api.model(
        "service_list",
        {
            "current_page": fields.Integer(),
            "total_items": fields.Integer(),
            "total_pages": fields.Integer(),
            "items": fields.List(fields.Nested(service_response)),
        },
    )
