from flask_restx import Namespace, fields

from app.main.model import OPERATION_TYPES
from app.main.service import CustomDateTime
from app.main.util.medical_prescription.medical_prescription_medicine_dto import (
    MedicalPrescriptionMedicineDTO,
)

_medical_prescription_medicine_medicine = (
    MedicalPrescriptionMedicineDTO.medical_prescription_medicine_medicine
)


class HistoryMedicalPrescriptionMedicineDTO:

    api = Namespace(
        "history_medical_prescription_medicine",
        description="history medical prescription medicine related operations",
    )

    history_medical_prescription_medicine = api.model(
        "history_medical_prescription_medicine",
        {
            "medical_prescription_medicine": fields.Nested(
                _medical_prescription_medicine_medicine
            ),
            "operation_type": fields.String(
                description="operation type", enum=OPERATION_TYPES
            ),
            "performed_at": CustomDateTime(
                description="medicine performed date and time",
            ),
        },
    )
