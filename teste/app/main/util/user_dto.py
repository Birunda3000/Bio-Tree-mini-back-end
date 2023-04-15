from flask_restx import Namespace, fields

from app.main.model import STATUS_OPTIONS


class UserDTO:

    api = Namespace("user", description="user related operations")

    user_post = api.model(
        "user_create",
        {
            "professional_id": fields.Integer(
                skip_none=True, required=True, description="professional relationship"
            ),
            "login": fields.String(required=True, description="user login"),
        },
    )

    user_put = api.model(
        "user_put",
        {
            "status": fields.String(
                required=True, description="user status", enum=["active", "blocked"]
            )
        },
    )

    user_response = api.model(
        "user_response",
        {
            "id": fields.Integer(description="user id"),
            "professional_id": fields.Integer(
                skip_none=True, description="professional relationship"
            ),
            "login": fields.String(description="user login"),
            "status": fields.String(description="user status", enum=STATUS_OPTIONS),
        },
    )

    user_list = api.model(
        "user_list",
        {
            "current_page": fields.Integer(),
            "total_items": fields.Integer(),
            "total_pages": fields.Integer(),
            "items": fields.List(fields.Nested(user_response)),
        },
    )
