from datetime import datetime

from sqlalchemy.orm.exc import NoResultFound
from werkzeug.datastructures import ImmutableMultiDict

from app.main import db
from app.main.exceptions import DefaultException
from app.main.model import (
    Action,
    AdmissionActionAssociation,
    AdmissionQuestionAssociation,
    Question,
    VitalSignsControl,
)

_HISTORY_TYPE = "Enfermagem"


def get_sae(params: ImmutableMultiDict):

    admission_id = params.get("admission_id", type=int)

    admission = get_admission(admission_id=admission_id)

    questions = (
        Question.query.join(AdmissionQuestionAssociation, isouter=True)
        .filter(
            AdmissionQuestionAssociation.question_id == Question.id,
            AdmissionQuestionAssociation.admission_id == admission.id,
        )
        .all()
    )

    actions = (
        Action.query.join(AdmissionActionAssociation, isouter=True)
        .with_entities(Action.id, Action.name, AdmissionActionAssociation.recurrence)
        .filter(
            AdmissionActionAssociation.action_id == Action.id,
            AdmissionActionAssociation.admission_id == admission.id,
        )
        .all()
    )

    return {"questions": questions, "actions": actions}


def save_sae(data: dict[str, any]) -> None:

    admission = get_admission(admission_id=data.get("admission_id"))

    professional = get_professional(professional_id=data.get("professional_id"))

    vital_signs = data.get("vital_signs_control")
    prescription_performed = data.get("prescriptions_performed")

    if not vital_signs and not prescription_performed:
        raise DefaultException("informations_empty", code=409)

    vital_sign_history = {}
    actions_history = []

    if prescription_performed:

        _validate_actions(
            actions_ids=set(
                [
                    prescription.get("action_id")
                    for prescription in prescription_performed
                ]
            )
        )

        for action in prescription_performed:

            try:
                action_association = AdmissionActionAssociation.query.filter_by(
                    admission_id=admission.id, action_id=action.get("action_id")
                ).one()
            except NoResultFound:
                raise DefaultException("action_not_found", code=404)

            if action.get("delete"):

                db.session.delete(action_association)

                actions_history.append(
                    {
                        "id": action.get("action_id"),
                        "performed_at": datetime_from_string(
                            action.get("performed_at")
                        ),
                        "operation_type": "Remoção",
                    }
                )

            else:

                actions_history.append(
                    {
                        "id": action.get("action_id"),
                        "performed_at": datetime_from_string(
                            action.get("performed_at")
                        ),
                        "operation_type": "Realização",
                    }
                )

    if vital_signs:

        new_vital_signs = VitalSignsControl(
            admission=admission,
            sys_blood_pressure=vital_signs.get("sys_blood_pressure"),
            dia_blood_pressure=vital_signs.get("dia_blood_pressure"),
            heart_pulse=vital_signs.get("heart_pulse"),
            respiratory_frequence=vital_signs.get("respiratory_frequence"),
            body_fat_rate=vital_signs.get("body_fat_rate"),
            temperature=vital_signs.get("temperature") or None,
            oxygen_saturation=vital_signs.get("oxygen_saturation") or None,
        )
        db.session.add(new_vital_signs)
        db.session.flush()

        vital_signs_performed_at = datetime_from_string(vital_signs.get("performed_at"))
        vital_sign_history = {
            "id": new_vital_signs.id,
            "performed_at": vital_signs_performed_at,
        }

    db.session.commit()

    save_new_history(
        admission_id=admission.id,
        professional_id=professional.id,
        type=_HISTORY_TYPE,
        nursing_prescription_vital_signs_control_data=vital_sign_history or None,
        nursing_prescription_actions_data=actions_history or None,
    )


def save_determinations(data: dict[str, any]) -> None:
    _actual_datetime = datetime.now()

    admission = get_admission(admission_id=data.get("admission_id"))

    professional = get_professional(professional_id=data.get("professional_id"))

    actions = data.get("actions")
    questions = data.get("questions")

    if not actions and not questions:
        raise DefaultException("determinations_empty", code=409)

    actions_history = []
    questions_history = []

    if actions:

        actions_id_recurrence_dict = dict(
            [(action.get("id"), action.get("recurrence")) for action in actions]
        )

        new_actions_ids = set(actions_id_recurrence_dict.keys())

        _validate_actions(actions_ids=new_actions_ids)

        _update_actions_already_registered(
            admission_id=admission.id,
            actions_id_recurrence_dict=actions_id_recurrence_dict,
        )

        if actions_id_recurrence_dict:

            actions_history = []
            for action_id, recurrence in actions_id_recurrence_dict.items():

                new_association = AdmissionActionAssociation(
                    admission=admission,
                    action_id=action_id,
                    recurrence=recurrence,
                )
                db.session.add(new_association)

                actions_history.append(
                    {
                        "id": action_id,
                        "performed_at": datetime_to_string(_actual_datetime),
                        "operation_type": "Adição",
                    }
                )

    if questions:

        new_questions_ids = set(questions)

        _validate_questions(questions_ids=new_questions_ids)

        questions_history = _delete_actual_diagnoses(admission_id=admission.id)

        for question in new_questions_ids:
            new_association = AdmissionQuestionAssociation(
                admission=admission, question_id=question
            )
            db.session.add(new_association)

            questions_history.append(
                {
                    "id": question,
                    "operation_type": "Adição",
                }
            )

    db.session.commit()

    save_new_history(
        admission_id=admission.id,
        professional_id=professional.id,
        type=_HISTORY_TYPE,
        nursing_prescription_actions_data=actions_history,
        nursing_prescription_questions_data=questions_history,
    )


def delete_questions(data: dict[str, any]) -> None:

    admission = get_admission(admission_id=data.get("admission_id"))

    professional = get_professional(professional_id=data.get("professional_id"))

    questions_ids = set(data.get("questions"))
    if not questions_ids:
        raise DefaultException("questions_empty", code=409)

    _validate_questions(questions_ids=questions_ids)

    actual_questions_association = AdmissionQuestionAssociation.query.filter(
        AdmissionQuestionAssociation.question_id.in_(questions_ids),
    ).all()

    deleted = []
    for question_associated in actual_questions_association:
        db.session.delete(question_associated)
        deleted.append(
            {"id": question_associated.question_id, "operation_type": "Remoção"}
        )

    db.session.commit()

    save_new_history(
        admission_id=admission.id,
        professional_id=professional.id,
        nursing_prescription_questions_data=deleted,
        type=_HISTORY_TYPE,
    )


def _delete_actual_diagnoses(admission_id: int) -> list[dict[str, any]]:
    actual_diagnoses = AdmissionQuestionAssociation.query.filter_by(
        admission_id=admission_id
    ).all()

    deleted = []
    for diagnosis in actual_diagnoses:
        db.session.delete(diagnosis)
        deleted.append({"id": diagnosis.question_id, "operation_type": "Remoção"})

    return deleted


def _update_actions_already_registered(
    admission_id: int, actions_id_recurrence_dict: dict
) -> None:

    actions_associated = (
        AdmissionActionAssociation.query.filter(
            AdmissionActionAssociation.action_id.in_(actions_id_recurrence_dict.keys()),
        )
        .filter_by(admission_id=admission_id)
        .all()
    )

    for association in actions_associated:
        association.recurrence = actions_id_recurrence_dict.get(association.action_id)
        actions_id_recurrence_dict.pop(association.action_id)
        db.session.add(association)


def _validate_actions(actions_ids: set[int]) -> None:

    actions = Action.query.filter(Action.id.in_(actions_ids)).all()

    actions_ids_db = set(action.id for action in actions)

    if actions_ids != actions_ids_db:
        raise DefaultException("action_not_found", code=404)


def _validate_questions(questions_ids: set[int]) -> None:

    questions = Question.query.filter(Question.id.in_(questions_ids)).all()

    questions_ids_db = set(question.id for question in questions)

    if questions_ids != questions_ids_db:
        raise DefaultException("question_not_found", code=404)


from app.main.service.admission_service import get_admission
from app.main.service.custom_fields import datetime_from_string, datetime_to_string
from app.main.service.history_service import save_new_history
from app.main.service.professional_service import get_professional
