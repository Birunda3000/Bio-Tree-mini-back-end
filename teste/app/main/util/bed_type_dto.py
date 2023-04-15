from flask_restx import Namespace, fields


class BedTypeDTO:
    api = Namespace("bed_type", description="bed type related operations")

    bed_type_post = api.model(
        "bed_type_post",
        {
            "name": fields.String(
                description="bed type name",
                min_length=1,
                required=True,
            ),
        },
    )

    bed_type_update = api.clone("bed_type_put", bed_type_post)

    bed_type_response = api.clone(
        "bed_type_response",
        bed_type_post,
        {"id": fields.Integer(description="bed type id")},
    )

    bed_type_list = api.model(
        "bed_type_list",
        {
            "current_page": fields.Integer(),
            "total_items": fields.Integer(),
            "total_pages": fields.Integer(),
            "items": fields.List(fields.Nested(bed_type_response)),
        },
    )
