from flask_restx import Namespace, fields

from app.main.util.medicine_dto import MedicineDTO

_medicine_name = MedicineDTO.medicine_name
from app.main.service import CustomDateTime


class MedicalPrescriptionMedicineDTO:

    api = Namespace(
        "medical_prescription_medicine",
        description="medical prescription medicine related operations",
    )

    medical_prescription_medicine_medicine = api.model(
        "medical_prescription_medicine_medicine",
        {
            "medicine": fields.Nested(_medicine_name),
        },
    )

    medical_prescription_medicine_response = api.model(
        "medical_prescription_medicine_response",
        {
            "medicine": fields.Nested(_medicine_name),
            "execute_at": CustomDateTime(
                description="medicine execution date and time",
            ),
            "observations": fields.String(
                description="medicine observation", example="Medicine Observation"
            ),
        },
    )

    medical_prescription_medicine_post = api.model(
        "medical_prescription_medicine_post",
        {
            "medicine_id": fields.Integer(
                required=True, description="medicine relationship", example=1
            ),
            "execute_at": CustomDateTime(
                required=True,
                description="medicine execution date and time",
            ),
            "observations": fields.String(
                description="medicine observation", example="Medicine Observation"
            ),
        },
    )
