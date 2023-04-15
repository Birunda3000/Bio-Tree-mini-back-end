from flask_restx import Namespace, fields

from app.main.model import ADMISSION_TYPES
from app.main.util.medical_prescription.medical_prescription_medicine_dto import (
    MedicalPrescriptionMedicineDTO,
)
from app.main.util.medical_prescription.medical_prescription_orientation_dto import (
    MedicalPrescriptionOrientationDTO,
)
from app.main.util.medical_prescription.medical_prescription_procedure_dto import (
    MedicalPrescriptionProcedureDTO,
)

_orientation_post = (
    MedicalPrescriptionOrientationDTO.medical_prescription_orientation_post
)
_medicine_post = MedicalPrescriptionMedicineDTO.medical_prescription_medicine_post
_procedure_post = MedicalPrescriptionProcedureDTO.medical_prescription_procedure_post
_orientation_response = (
    MedicalPrescriptionOrientationDTO.medical_prescription_orientation_response
)
_medicine_response = (
    MedicalPrescriptionMedicineDTO.medical_prescription_medicine_response
)
_procedure_response = (
    MedicalPrescriptionProcedureDTO.medical_prescription_procedure_response
)


class MedicalPrescriptionDTO:

    api = Namespace(
        "medical_prescription", description="medical prescription related operations"
    )

    medical_prescription_post = api.model(
        "medical_prescription_post",
        {
            "professional_id": fields.Integer(
                required=True, description="professional relationship", example=1
            ),
            "patient_id": fields.Integer(
                required=True, description="patient relationship", example=1
            ),
            "room_id": fields.Integer(
                required=True, description="room relationship", example=1
            ),
            "type": fields.String(
                required=True, description="admission type", enum=ADMISSION_TYPES
            ),
            "orientations": fields.List(fields.Nested(_orientation_post)),
            "medicines": fields.List(fields.Nested(_medicine_post)),
            "procedures": fields.List(fields.Nested(_procedure_post)),
        },
    )

    medical_prescription_response = api.model(
        "medical_prescription_response",
        {
            "id": fields.Integer(description="medical prescription id"),
            "professional_id": fields.Integer(
                required=True, description="professional relationship", example=1
            ),
            "patient_id": fields.Integer(
                required=True, description="patient relationship", example=1
            ),
            "room_id": fields.Integer(
                required=True, description="room relationship", example=1
            ),
            "orientations": fields.List(fields.Nested(_orientation_response)),
            "medicines": fields.List(fields.Nested(_medicine_response)),
            "procedures": fields.List(fields.Nested(_procedure_response)),
        },
    )

    medical_prescription_list = api.model(
        "medical_prescription_list",
        {
            "current_page": fields.Integer(),
            "total_items": fields.Integer(),
            "total_pages": fields.Integer(),
            "items": fields.List(fields.Nested(medical_prescription_response)),
        },
    )
