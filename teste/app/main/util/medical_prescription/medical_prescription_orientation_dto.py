from flask_restx import Namespace, fields

from app.main.service import CustomDateTime


class MedicalPrescriptionOrientationDTO:

    api = Namespace(
        "medical_prescription_orientation",
        description="medical prescription orientation related operations",
    )

    medical_prescription_orientation_orientation = api.model(
        "medical_prescription_orientation_orientation",
        {
            "orientation": fields.String(
                description="prescription", example="Orientation"
            ),
        },
    )

    medical_prescription_orientation_response = api.model(
        "medical_prescription_orientation_response",
        {
            "id": fields.Integer(description="orientation relationship", example=1),
            "orientation": fields.String(
                description="prescription", example="Medicine"
            ),
            "execute_at": CustomDateTime(
                description="medicine execution date and time",
            ),
            "observations": fields.String(
                description="orientation observation", example="Orientation Observation"
            ),
        },
    )

    medical_prescription_orientation_post = api.model(
        "medical_prescription_orientation_post",
        {
            "orientation": fields.String(
                required=True, description="prescription", example="Orientation"
            ),
            "execute_at": CustomDateTime(
                required=True,
                description="medicine execution date and time",
            ),
            "observations": fields.String(
                description="orientation observation", example="Orientation Observation"
            ),
        },
    )
