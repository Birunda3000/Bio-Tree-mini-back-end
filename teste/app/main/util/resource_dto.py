from flask_restx import Namespace, fields


class ResourceDTO:
    api = Namespace("resource", description="resource related operations")

    resource_role_response = api.model(
        "resource_by_role",
        {
            "id": fields.Integer(description="resource id"),
            "name": fields.String(description="resource name"),
        },
    )

    resource_response = api.clone(
        "resource",
        resource_role_response,
        {
            "code": fields.String(description="resource code"),
        },
    )
