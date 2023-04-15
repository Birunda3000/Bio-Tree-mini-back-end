from flask_restx import Namespace, fields

from app.main.model import OPERATION_TYPES
from app.main.util.medical_prescription.medical_prescription_procedure_dto import (
    MedicalPrescriptionProcedureDTO,
)

_medical_prescription_procedure_description = (
    MedicalPrescriptionProcedureDTO.medical_prescription_procedure_description
)
from app.main.service import CustomDateTime


class HistoryMedicalPrescriptionProcedureDTO:

    api = Namespace(
        "history_medical_prescription_procedure",
        description="history medical prescription procedure related operations",
    )

    history_medical_prescription_procedure = api.model(
        "history_medical_prescription_procedure",
        {
            "medical_prescription_procedure": fields.Nested(
                _medical_prescription_procedure_description
            ),
            "operation_type": fields.String(
                description="operation type", enum=OPERATION_TYPES
            ),
            "performed_at": CustomDateTime(
                description="procedure performed date and time",
            ),
        },
    )
