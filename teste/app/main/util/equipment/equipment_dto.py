from flask_restx import Namespace, fields

from app.main.util.equipment.equipment_type_dto import EquipmentTypeDTO

_type_response = EquipmentTypeDTO.equipment_type_response


class EquipmentDTO:
    api = Namespace("equipment", description="equipment related operations")

    equipment_post = api.model(
        "equipment_post",
        {
            "name": fields.String(
                required=True,
                description="equipment name",
                min_length=1,
            ),
            "equipment_type_id": fields.Integer(
                required=True, description="equipment type relationship", min=0
            ),
        },
    )

    equipment_response = api.model(
        "equipment_response",
        {
            "id": fields.Integer(description="equipment id"),
            "name": fields.String(description="equipment name"),
            "equipment_type": fields.Nested(
                _type_response, description="equipment type data"
            ),
        },
    )

    equipment_list = api.model(
        "equipment_list",
        {
            "current_page": fields.Integer(),
            "total_items": fields.Integer(),
            "total_pages": fields.Integer(),
            "items": fields.List(fields.Nested(equipment_response)),
        },
    )
