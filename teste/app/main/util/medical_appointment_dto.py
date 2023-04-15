from flask_restx import Namespace, fields

from app.main.model import DIAGNOSIS_RELATED_WORK_OR_TRAFFIC, DIAGNOSIS_TYPES


class MedicalAppointmentDTO:

    api = Namespace(
        "medical appointment", description="medical appointment related operations"
    )

    medical_appointment_post = api.model(
        "medical_appointment_post",
        {
            "patient_id": fields.Integer(
                required=True, description="patient relationship", example=1
            ),
            "professional_id": fields.Integer(
                required=True, description="professional relationship", example=1
            ),
            "description": fields.String(
                required=True, description="patient medical description"
            ),
            "diagnosis_type": fields.String(
                required=True, description="diagnosis type", enum=DIAGNOSIS_TYPES
            ),
            "diagnosis_work": fields.String(
                required=True,
                description="diagnosis related to work",
                enum=DIAGNOSIS_RELATED_WORK_OR_TRAFFIC,
            ),
            "diagnosis_traffic_accident": fields.String(
                required=True,
                description="diagnosis related to traffic accident",
                enum=DIAGNOSIS_RELATED_WORK_OR_TRAFFIC,
            ),
        },
    )

    medical_appointment_response = api.clone(
        "medical_appointment_response",
        medical_appointment_post,
        {"id": fields.Integer(description="medical appointment id")},
    )

    medical_appointment_list = api.model(
        "medical_appointment_list",
        {
            "current_page": fields.Integer(),
            "total_items": fields.Integer(),
            "total_pages": fields.Integer(),
            "items": fields.List(fields.Nested(medical_appointment_response)),
        },
    )
