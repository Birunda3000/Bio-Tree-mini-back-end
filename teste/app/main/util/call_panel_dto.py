from flask_restx import Namespace, fields


class CallPanelDTO:
    api = Namespace("call_panel", description="call panel related operations")

    call_panel_post = api.model(
        "call panel create",
        {
            "name": fields.String(
                required=True, description="call panel name", min_length=1
            ),
        },
    )

    call_panel_response = api.clone(
        "call panel response",
        call_panel_post,
        {"id": fields.Integer(description="call panel id")},
    )

    call_panel_list = api.model(
        "call panel list",
        {
            "current_page": fields.Integer(description="current page"),
            "total_items": fields.Integer(description="total items"),
            "total_pages": fields.Integer(description="total pages"),
            "items": fields.List(fields.Nested(call_panel_response)),
        },
    )
