from flask_restx import Namespace, fields


class EquipmentTypeDTO:
    api = Namespace("equipment_type", description="equipment type related operations")

    equipment_type_post = api.model(
        "equipment_type_post",
        {
            "name": fields.String(
                required=True,
                description="equipment type name",
                min_length=1,
            )
        },
    )

    equipment_type_update = api.clone("equipment_type_put", equipment_type_post)

    equipment_type_response = api.clone(
        "equipment_type_response",
        equipment_type_post,
        {"id": fields.Integer(description="equipment type id")},
    )

    equipment_type_list = api.model(
        "equipment_type_list",
        {
            "current_page": fields.Integer(),
            "total_items": fields.Integer(),
            "total_pages": fields.Integer(),
            "items": fields.List(fields.Nested(equipment_type_response)),
        },
    )
