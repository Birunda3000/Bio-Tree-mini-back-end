from flask_restx import Namespace, fields


class AuthDTO:
    api = Namespace("auth", description="Authentication related operations")

    auth_response = api.model(
        "login_response",
        {
            "token": fields.String(description="User JWT"),
            "professional_name": fields.String(description="Professional name"),
            "professional_id": fields.Integer(description="Professional ID"),
        },
    )

    auth = api.model(
        "login",
        {
            "login": fields.String(
                required=True, description="user login", max_length=128
            ),
            "password": fields.String(
                required=True, description="user password", min_length=8
            ),
        },
    )
