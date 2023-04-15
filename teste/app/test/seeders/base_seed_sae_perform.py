from app.main.model import (
    History,
    HistoryNursingPrescriptionAction,
    HistoryNursingPrescriptionQuestion,
    HistoryNursingPrescriptionVitalSignsControl,
)
from app.main.service import datetime_from_string


def create_base_seed_sae_perform(db):

    new_history = History(admission_id=1, professional_id=1, type="Enfermagem")

    new_history.nursing_prescription_vital_signs_control = (
        HistoryNursingPrescriptionVitalSignsControl(
            vital_signs_control_id=1,
            performed_at=datetime_from_string("17/11/2022 22:15:00"),
        )
    )

    new_history_nursing_prescription_question = HistoryNursingPrescriptionQuestion(
        question_id=1,
        operation_type="Adição",
    )

    new_history.nursing_prescription_questions.append(
        new_history_nursing_prescription_question
    )

    new_history_nursing_prescription_question = HistoryNursingPrescriptionQuestion(
        question_id=2,
        operation_type="Adição",
    )

    new_history.nursing_prescription_questions.append(
        new_history_nursing_prescription_question
    )

    new_history_nursing_prescription_action = HistoryNursingPrescriptionAction(
        action_id=1,
        operation_type="Adição",
        performed_at=datetime_from_string("17/11/2022 22:15:00"),
    )

    new_history.nursing_prescription_actions.append(
        new_history_nursing_prescription_action
    )

    db.session.add(new_history)

    new_history = History(admission_id=2, professional_id=2, type="Enfermagem")

    new_history_nursing_prescription_question = HistoryNursingPrescriptionQuestion(
        question_id=1,
        operation_type="Remoção",
    )

    new_history.nursing_prescription_questions.append(
        new_history_nursing_prescription_question
    )

    new_history_nursing_prescription_question = HistoryNursingPrescriptionQuestion(
        question_id=2,
        operation_type="Adição",
    )

    new_history.nursing_prescription_questions.append(
        new_history_nursing_prescription_question
    )

    new_history_nursing_prescription_action = HistoryNursingPrescriptionAction(
        action_id=1,
        operation_type="Remoção",
        performed_at=datetime_from_string("17/11/2022 22:15:00"),
    )

    new_history.nursing_prescription_actions.append(
        new_history_nursing_prescription_action
    )

    db.session.add(new_history)

    db.session.commit()
