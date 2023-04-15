from flask_restx import Namespace, fields

from app.main.model import OPERATION_TYPES
from app.main.service import CustomDateTime
from app.main.util.medical_prescription.medical_prescription_orientation_dto import (
    MedicalPrescriptionOrientationDTO,
)

_medical_prescription_orientation_orientation = (
    MedicalPrescriptionOrientationDTO.medical_prescription_orientation_orientation
)


class HistoryMedicalPrescriptionOrientationDTO:

    api = Namespace(
        "history_medical_prescription_orientation",
        description="history medical prescription orientation related operations",
    )

    history_medical_prescription_orientation = api.model(
        "history_medical_prescription_orientation",
        {
            "medical_prescription_orientation": fields.Nested(
                _medical_prescription_orientation_orientation
            ),
            "operation_type": fields.String(
                description="operation type", enum=OPERATION_TYPES
            ),
            "performed_at": CustomDateTime(
                description="orientation performed date and time",
            ),
        },
    )
