from flask_restx import Namespace, fields


class ItemClassificationDTO:
    api = Namespace(
        "Item_classification", description="Item classification related operations"
    )

    item_classification_post = api.model(
        "Item_classification_post",
        {
            "name": fields.String(
                required=True,
                description="Item classification name",
                min_length=1,
            )
        },
    )

    item_classification_update = api.clone(
        "Item_classification_put", item_classification_post
    )

    item_classification_response = api.clone(
        "Item_classification_response",
        item_classification_post,
        {"id": fields.Integer(description="Item classification id")},
    )

    item_classifications_list = api.model(
        "Item_classification_list",
        {
            "current_page": fields.Integer(),
            "total_items": fields.Integer(),
            "total_pages": fields.Integer(),
            "items": fields.List(fields.Nested(item_classification_response)),
        },
    )
