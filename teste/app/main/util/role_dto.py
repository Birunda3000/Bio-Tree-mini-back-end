from flask_restx import Namespace, fields

from app.main.service import RESOURCES_NAME, create_code
from app.main.util.resource_dto import ResourceDTO

_resource_response = ResourceDTO.resource_role_response


class RoleDTO:
    api = Namespace("role", description="role related operations")

    role_post = api.model(
        "role",
        {
            "name": fields.String(required=True, description="role name", min_length=1),
            "resources": fields.List(
                fields.String(
                    enum=[create_code(resource) for resource in RESOURCES_NAME]
                ),
                required=True,
                description="List of resources",
            ),
        },
    )

    role_response = api.model(
        "role response",
        {
            "id": fields.Integer(description="role id"),
            "name": fields.String(description="role name"),
            "resources": fields.List(
                fields.Nested(_resource_response), description="role resources"
            ),
            "is_default": fields.Boolean,
        },
    )
