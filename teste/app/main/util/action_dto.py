from flask_restx import Namespace, fields


class ActionDTO:
    api = Namespace("action", description="action related operations")

    action_name = api.model(
        "action_name",
        {
            "name": fields.String(description="action name"),
        },
    )

    action_post = api.model(
        "action_create",
        {"name": fields.String(required=True, description="action name", min_length=1)},
    )

    action_response = api.clone(
        "action_response", action_post, {"id": fields.Integer(description="action id")}
    )

    action_list = api.model(
        "action_list",
        {
            "current_page": fields.Integer(),
            "total_items": fields.Integer(),
            "total_pages": fields.Integer(),
            "items": fields.List(fields.Nested(action_response)),
        },
    )
