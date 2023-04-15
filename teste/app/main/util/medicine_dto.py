from flask_restx import Namespace, fields


class MedicineDTO:
    api = Namespace("medicine", description="medicine related operations")

    medicine_post = api.model(
        "medicine_create",
        {
            "name": fields.String(
                required=True, description="medicine name", min_length=1
            )
        },
    )

    medicine_put = api.clone("medicine_put", medicine_post)

    medicine_response = api.model(
        "medicine_response",
        {
            "id": fields.Integer(description="medicine id", example=1),
            "name": fields.String(description="medicine name"),
        },
    )

    medicine_name = api.model(
        "medicine_name",
        {
            "id": fields.Integer(description="medicine id", example=1),
            "name": fields.String(description="medicine name"),
        },
    )

    medicine_list = api.model(
        "medicine_list",
        {
            "current_page": fields.Integer(),
            "total_items": fields.Integer(),
            "total_pages": fields.Integer(),
            "items": fields.List(fields.Nested(medicine_response)),
        },
    )
