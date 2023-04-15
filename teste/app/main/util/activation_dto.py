from flask_restx import Namespace, fields


class ActivationDTO:

    api = Namespace("activation", description="activation related operations")

    activation_post = api.model(
        "activation resend",
        {
            "new_password": fields.String(
                required=True, description="new user password", min_length=8
            ),
            "repeat_new_password": fields.String(
                required=True, description="repeat new user password", min_length=8
            ),
        },
    )
