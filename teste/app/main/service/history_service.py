from math import ceil

from werkzeug.datastructures import ImmutableMultiDict

from app.main import db
from app.main.config import Config
from app.main.exceptions import DefaultException, ValidationException
from app.main.model import (
    HISTORY_TYPES,
    Action,
    Admission,
    History,
    HistoryMedicalPrescriptionMedicine,
    HistoryMedicalPrescriptionOrientation,
    HistoryMedicalPrescriptionProcedure,
    HistoryNursingPrescriptionAction,
    HistoryNursingPrescriptionQuestion,
    HistoryNursingPrescriptionVitalSignsControl,
    MedicalPrescriptionMedicine,
    MedicalPrescriptionOrientation,
    MedicalPrescriptionProcedure,
    Professional,
    Question,
    VitalSignsControl,
)

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def get_histories(params: ImmutableMultiDict):
    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)
    admission_id = params.get("admission_id", type=int)
    professional_id = params.get("professional_id", type=int)
    type = params.get("type", type=str)

    filters = []

    if admission_id:
        filters.append(History.admission_id == admission_id)
    if professional_id:
        filters.append(History.professional_id == professional_id)
    if type:
        filters.append(History.type == type)

    pagination = (
        History.query.filter(*filters)
        .order_by(History.id)
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return {
        "current_page": page,
        "total_items": pagination.total,
        "total_pages": ceil(pagination.total / per_page),
        "items": pagination.items,
    }


def save_new_history(
    admission_id: int,
    professional_id: int,
    type: str,
    nursing_prescription_vital_signs_control_data: dict[str, any] = None,
    nursing_prescription_questions_data: list = None,
    nursing_prescription_actions_data: list = None,
    medical_prescription_medicines_data: list = None,
    medical_prescription_orientations_data: list = None,
    medical_prescription_procedures_data: list = None,
) -> None:
    admission = get_admission(admission_id=admission_id)

    professional = get_professional(professional_id=professional_id)

    _valid_history_type_or_400(history_type=type)

    if nursing_prescription_vital_signs_control_data:
        _nursing_prescription_vital_signs_control_exists(
            nursing_prescription_vital_signs_control=nursing_prescription_vital_signs_control_data
        )

    if nursing_prescription_questions_data:
        _nursing_prescription_questions_exist(
            nursing_prescription_questions=nursing_prescription_questions_data
        )

    if nursing_prescription_actions_data:
        _nursing_prescription_actions_exist(
            nursing_prescription_actions=nursing_prescription_actions_data
        )

    if medical_prescription_medicines_data:
        _medical_prescription_medicines_exist(
            medical_prescription_medicines=medical_prescription_medicines_data
        )

    if medical_prescription_orientations_data:
        _medical_prescription_orientations_exist(
            medical_prescription_orientations=medical_prescription_orientations_data
        )

    if medical_prescription_procedures_data:
        _medical_prescription_procedures_exist(
            medical_prescription_procedures=medical_prescription_procedures_data
        )

    new_history = History(admission=admission, professional=professional, type=type)

    if nursing_prescription_vital_signs_control_data:
        _add_nursing_prescription_vital_signs_control(
            data=nursing_prescription_vital_signs_control_data, history=new_history
        )

    if nursing_prescription_questions_data:

        _add_nursing_prescription_questions(
            data=nursing_prescription_questions_data, history=new_history
        )

    if nursing_prescription_actions_data:

        _add_nursing_prescription_actions(
            data=nursing_prescription_actions_data, history=new_history
        )

    if medical_prescription_medicines_data:

        _add_medical_prescription_medicines(
            data=medical_prescription_medicines_data, history=new_history
        )

    if medical_prescription_orientations_data:

        _add_medical_prescription_orientations(
            data=medical_prescription_orientations_data, history=new_history
        )

    if medical_prescription_procedures_data:

        _add_medical_prescription_procedures(
            data=medical_prescription_procedures_data, history=new_history
        )

    db.session.add(new_history)
    db.session.commit()


def _nursing_prescription_vital_signs_control_exists(
    nursing_prescription_vital_signs_control: dict[str, any],
) -> None:
    get_vital_signs_control(
        vital_signs_control_id=nursing_prescription_vital_signs_control.get("id")
    )


def _nursing_prescription_actions_exist(nursing_prescription_actions: list) -> None:
    if nursing_prescription_actions:
        nursing_prescription_actions_ids = set(
            [
                nursing_prescription_action.get("id")
                for nursing_prescription_action in nursing_prescription_actions
            ]
        )
        nursing_prescription_actions_db = Action.query.filter(
            Action.id.in_(nursing_prescription_actions_ids)
        ).all()
        nursing_prescription_actions_ids_db = set(
            [
                nursing_prescription_action.id
                for nursing_prescription_action in nursing_prescription_actions_db
            ]
        )
        if nursing_prescription_actions_ids != nursing_prescription_actions_ids_db:
            raise DefaultException("action_not_found", code=404)


def _nursing_prescription_questions_exist(
    nursing_prescription_questions: list,
) -> None:
    if nursing_prescription_questions:
        nursing_prescription_questions_ids = set(
            [
                nursing_prescription_question.get("id")
                for nursing_prescription_question in nursing_prescription_questions
            ]
        )
        nursing_prescription_questions_db = Question.query.filter(
            Question.id.in_(nursing_prescription_questions_ids)
        ).all()
        nursing_prescription_questions_ids_db = set(
            [
                nursing_prescription_question.id
                for nursing_prescription_question in nursing_prescription_questions_db
            ]
        )
        if nursing_prescription_questions_ids != nursing_prescription_questions_ids_db:
            raise DefaultException("question_not_found", code=404)


def _medical_prescription_medicines_exist(medical_prescription_medicines: list) -> None:
    if medical_prescription_medicines:
        medical_prescription_medicines_ids = set(
            [
                medical_prescription_medicine.get("id")
                for medical_prescription_medicine in medical_prescription_medicines
            ]
        )
        medical_prescription_medicines_db = MedicalPrescriptionMedicine.query.filter(
            MedicalPrescriptionMedicine.id.in_(medical_prescription_medicines_ids)
        ).all()
        medical_prescription_medicines_ids_db = set(
            [
                medical_prescription_medicine.id
                for medical_prescription_medicine in medical_prescription_medicines_db
            ]
        )
        if medical_prescription_medicines_ids != medical_prescription_medicines_ids_db:
            raise DefaultException("medical_prescription_medicine_not_found", code=404)


def _medical_prescription_orientations_exist(
    medical_prescription_orientations: list,
) -> None:
    if medical_prescription_orientations:
        medical_prescription_orientations_ids = set(
            [
                medical_prescription_orientation.get("id")
                for medical_prescription_orientation in medical_prescription_orientations
            ]
        )
        medical_prescription_orientations_db = (
            MedicalPrescriptionOrientation.query.filter(
                MedicalPrescriptionOrientation.id.in_(
                    medical_prescription_orientations_ids
                )
            ).all()
        )
        medical_prescription_orientations_ids_db = set(
            [
                medical_prescription_orientation.id
                for medical_prescription_orientation in medical_prescription_orientations_db
            ]
        )
        if (
            medical_prescription_orientations_ids
            != medical_prescription_orientations_ids_db
        ):
            raise DefaultException(
                "medical_prescription_orientation_not_found", code=404
            )


def _medical_prescription_procedures_exist(
    medical_prescription_procedures: list,
) -> None:
    if medical_prescription_procedures:
        medical_prescription_procedures_ids = set(
            [
                medical_prescription_procedure.get("id")
                for medical_prescription_procedure in medical_prescription_procedures
            ]
        )
        medical_prescription_procedures_db = MedicalPrescriptionProcedure.query.filter(
            MedicalPrescriptionProcedure.id.in_(medical_prescription_procedures_ids)
        ).all()
        medical_prescription_procedures_ids_db = set(
            [
                medical_prescription_procedure.id
                for medical_prescription_procedure in medical_prescription_procedures_db
            ]
        )
        if (
            medical_prescription_procedures_ids
            != medical_prescription_procedures_ids_db
        ):
            raise DefaultException("medical_prescription_procedure_not_found", code=404)


def _add_nursing_prescription_vital_signs_control(
    data: dict[str, any], history: History
):
    HistoryNursingPrescriptionVitalSignsControl(
        history=history,
        vital_signs_control_id=data.get("id"),
        performed_at=data.get("performed_at"),
    )


def _add_nursing_prescription_questions(data: dict[str, any], history: History):
    for nursing_prescription_questions in data:
        new_history_nursing_prescription_question = HistoryNursingPrescriptionQuestion(
            question_id=nursing_prescription_questions.get("id"),
            operation_type=nursing_prescription_questions.get("operation_type"),
        )

        history.nursing_prescription_questions.append(
            new_history_nursing_prescription_question
        )


def _add_nursing_prescription_actions(data: dict[str, any], history: History):
    for nursing_prescription_actions in data:
        new_history_nursing_prescription_action = HistoryNursingPrescriptionAction(
            action_id=nursing_prescription_actions.get("id"),
            operation_type=nursing_prescription_actions.get("operation_type"),
            performed_at=nursing_prescription_actions.get("performed_at"),
        )

        history.nursing_prescription_actions.append(
            new_history_nursing_prescription_action
        )


def _add_medical_prescription_medicines(data: dict[str, any], history: History):
    for medical_prescription_medicine in data:
        new_history_medical_prescription_medicine = HistoryMedicalPrescriptionMedicine(
            medical_prescription_medicine_id=medical_prescription_medicine.get("id"),
            operation_type=medical_prescription_medicine.get("operation_type"),
            performed_at=datetime_from_string(
                medical_prescription_medicine.get("performed_at")
            ),
        )

        history.medical_prescription_medicines.append(
            new_history_medical_prescription_medicine
        )


def _add_medical_prescription_orientations(data: dict[str, any], history: History):
    for medical_prescription_orientation in data:
        new_history_medical_prescription_orientation = HistoryMedicalPrescriptionOrientation(
            medical_prescription_orientation_id=medical_prescription_orientation.get(
                "id"
            ),
            operation_type=medical_prescription_orientation.get("operation_type"),
            performed_at=datetime_from_string(
                medical_prescription_orientation.get("performed_at"),
            ),
        )

        history.medical_prescription_orientations.append(
            new_history_medical_prescription_orientation
        )


def _add_medical_prescription_procedures(data: dict[str, any], history: History):
    for medical_prescription_procedure in data:
        new_history_medical_prescription_procedure = (
            HistoryMedicalPrescriptionProcedure(
                medical_prescription_procedure_id=medical_prescription_procedure.get(
                    "id"
                ),
                operation_type=medical_prescription_procedure.get("operation_type"),
                performed_at=datetime_from_string(
                    medical_prescription_procedure.get("performed_at"),
                ),
            )
        )

        history.medical_prescription_procedures.append(
            new_history_medical_prescription_procedure
        )


def _valid_history_type_or_400(history_type: str) -> None:
    if not history_type in HISTORY_TYPES:
        raise ValidationException(
            errors={
                "history_type": "The history type must be of one valid history type."
            },
            message="history_type_invalid",
        )


from app.main.service.admission_service import get_admission
from app.main.service.custom_fields import datetime_from_string
from app.main.service.professional_service import get_professional
from app.main.service.vital_signs_control_service import get_vital_signs_control
