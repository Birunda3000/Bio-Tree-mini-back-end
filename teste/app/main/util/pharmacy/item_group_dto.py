from flask_restx import Namespace, fields


class ItemGroupDTO:
    api = Namespace("item_group", description="item group related operations")

    item_group_id = {"id": fields.Integer(description="item group id")}

    item_group_name = {
        "name": fields.String(
            required=True, description="item group name", min_length=1
        )
    }

    item_group_post = api.model("item_group_post", item_group_name)

    item_group_update = api.clone("item_group_put", item_group_post)

    item_group_response = api.clone(
        "item_group_response", item_group_id, item_group_post
    )

    item_group_list = api.model(
        "item_group_list",
        {
            "current_page": fields.Integer(),
            "total_items": fields.Integer(),
            "total_pages": fields.Integer(),
            "items": fields.List(fields.Nested(item_group_response)),
        },
    )
