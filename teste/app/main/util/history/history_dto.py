from flask_restx import Namespace, fields

from app.main.service import CustomDateTime
from app.main.util.history.history_medical_prescription_medicine_dto import (
    HistoryMedicalPrescriptionMedicineDTO,
)
from app.main.util.history.history_medical_prescription_orientation_dto import (
    HistoryMedicalPrescriptionOrientationDTO,
)
from app.main.util.history.history_medical_prescription_procedure_dto import (
    HistoryMedicalPrescriptionProcedureDTO,
)
from app.main.util.history.history_nursing_prescription_action_dto import (
    HistoryNursingPrescriptionActionDTO,
)
from app.main.util.history.history_nursing_prescription_question_dto import (
    HistoryNursingPrescriptionQuestionDTO,
)
from app.main.util.history.history_nursing_prescription_vital_signs_control_dto import (
    HistoryNursingPrescriptionVitalSignsControlDTO,
)
from app.main.util.professional_dto import ProfessionalDTO

_history_medical_prescription_medicine = (
    HistoryMedicalPrescriptionMedicineDTO.history_medical_prescription_medicine
)

_history_medical_prescription_orientation = (
    HistoryMedicalPrescriptionOrientationDTO.history_medical_prescription_orientation
)

_history_medical_prescription_procedure = (
    HistoryMedicalPrescriptionProcedureDTO.history_medical_prescription_procedure
)

_history_nursing_prescription_question = (
    HistoryNursingPrescriptionQuestionDTO.history_nursing_prescription_question
)

_history_nursing_prescription_action = (
    HistoryNursingPrescriptionActionDTO.history_nursing_prescription_action
)

_history_nursing_prescription_vital_signs_control = (
    HistoryNursingPrescriptionVitalSignsControlDTO.history_nursing_prescription_vitalsignscontrol
)


class HistoryDTO:
    api = Namespace("history", description="history related operations")

    history_response = api.model(
        "history_response",
        {
            "id": fields.Integer(description="history id", example=1),
            "admission_id": fields.Integer(
                description="admission relationship", example=1
            ),
            "professional": fields.Nested(
                api.model(
                    "history_response_professional", ProfessionalDTO.professional_name
                )
            ),
            "type": fields.String(description="history type", example="Observação"),
            "created_at": CustomDateTime(
                description="history creation date and time",
            ),
            "nursing_prescription_vital_signs_control": fields.Nested(
                _history_nursing_prescription_vital_signs_control
            ),
            "nursing_prescription_questions": fields.List(
                fields.Nested(_history_nursing_prescription_question)
            ),
            "nursing_prescription_actions": fields.List(
                fields.Nested(_history_nursing_prescription_action)
            ),
            "medical_prescription_medicines": fields.List(
                fields.Nested(_history_medical_prescription_medicine)
            ),
            "medical_prescription_orientations": fields.List(
                fields.Nested(_history_medical_prescription_orientation)
            ),
            "medical_prescription_procedures": fields.List(
                fields.Nested(_history_medical_prescription_procedure)
            ),
        },
    )

    history_list = api.model(
        "history_list",
        {
            "current_page": fields.Integer(),
            "total_items": fields.Integer(),
            "total_pages": fields.Integer(),
            "items": fields.List(fields.Nested(history_response)),
        },
    )
