from flask_restx import Namespace, fields


class UnitMeasurementDTO:
    api = Namespace(
        "unit measurement", description="unit measurement related operations"
    )

    unit_measurement_post = api.model(
        "unit measurement post",
        {
            "name": fields.String(
                required=True, description="unit measurement name", min_length=1
            )
        },
    )

    unit_measurement_update = api.clone("unit measurement put", unit_measurement_post)

    unit_measurement_response = api.clone(
        "unit measurement response",
        unit_measurement_post,
        {"id": fields.Integer(description="unit measurement id")},
    )

    unit_measurements_list = api.model(
        "unit measurement list",
        {
            "current_page": fields.Integer(),
            "total_items": fields.Integer(),
            "total_pages": fields.Integer(),
            "items": fields.List(fields.Nested(unit_measurement_response)),
        },
    )
