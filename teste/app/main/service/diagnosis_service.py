from math import ceil

from sqlalchemy.orm import joinedload
from werkzeug.datastructures import ImmutableMultiDict

from app.main import db
from app.main.config import Config
from app.main.exceptions import DefaultException
from app.main.model import Diagnosis, Protocol, Question

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def get_diagnoses(params: ImmutableMultiDict) -> dict[str, any]:
    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)
    protocol = params.get("protocol")

    filters = []
    if protocol:
        filters.append(Protocol.name.ilike(f"%{protocol}%")),

    pagination = (
        Diagnosis.query.options(joinedload("questions"), joinedload("protocol"))
        .join("protocol")
        .filter(*filters)
        .order_by(Diagnosis.id)
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return {
        "current_page": page,
        "total_items": pagination.total,
        "total_pages": ceil(pagination.total / per_page),
        "items": pagination.items,
    }


def get_diagnosis_by_id(diagnosis_id: int) -> None:

    get_diagnosis(diagnosis_id=diagnosis_id)

    filters = [Diagnosis.id == diagnosis_id]

    diagnosis_filtered = (
        Diagnosis.query.options(joinedload("questions"), joinedload("protocol"))
        .filter(*filters)
        .first()
    )

    questions_array = []

    for question in diagnosis_filtered.questions:

        questions_array.append(question.name)

    diagnosis_return = {
        "protocol": {
            "name": diagnosis_filtered.protocol.name,
            "protocol_type": diagnosis_filtered.protocol.protocol_type,
        },
        "questions": questions_array,
    }
    return diagnosis_return


def save_new_diagnosis(data: dict[str, any]):

    protocol = get_protocol(
        protocol_id=data.get("protocol_id"), options=[joinedload("diagnosis")]
    )
    if protocol.protocol_type != "Diagnóstico":
        raise DefaultException("protocol_is_not_diagnosis_type", code=409)
    if protocol.diagnosis:
        raise DefaultException("protocol_already_associated_with_diagnosis", code=409)

    questions = Question.query.filter(Question.id.in_(data.get("questions_ids"))).all()

    questions_ids = set(data.get("questions_ids"))

    questions_ids_db = set(question.id for question in questions)

    if questions_ids != questions_ids_db:
        raise DefaultException("question_not_found", code=404)

    new_diagnosis = Diagnosis(protocol_id=protocol.id, questions=questions)

    db.session.add(new_diagnosis)
    db.session.commit()


def update_diagnosis(diagnosis_id: int, data: dict[str, any]) -> None:

    diagnosis = get_diagnosis(
        diagnosis_id=diagnosis_id, options=[joinedload("questions")]
    )

    if change_protocol := diagnosis.protocol_id != data.get("protocol_id"):
        new_protocol = _get_protocol_and_validate(protocol_id=data.get("protocol_id"))

    new_questions_ids = set(data.get("questions_ids"))

    diagnosis_question_ids = set(diagnosis.id for diagnosis in diagnosis.questions)

    if diagnosis_question_ids != new_questions_ids:
        new_questions = _get_questions_and_validate(questions_ids=new_questions_ids)
        diagnosis.questions = new_questions

    if change_protocol:
        diagnosis.protocol = new_protocol

    db.session.commit()


def delete_diagnosis(diagnosis_id: int) -> None:

    diagnosis = get_diagnosis(diagnosis_id=diagnosis_id)

    db.session.delete(diagnosis)
    db.session.commit()


def _get_protocol_and_validate(protocol_id: int) -> Protocol:

    protocol = get_protocol(protocol_id=protocol_id, options=[joinedload("diagnosis")])
    if protocol.protocol_type != "Diagnóstico":
        raise DefaultException("protocol_is_not_diagnosis_type", code=409)
    if protocol.diagnosis:
        raise DefaultException("protocol_already_associated_with_diagnosis", code=409)

    return protocol


def _get_questions_and_validate(questions_ids: set[int]) -> list[Question]:

    questions = Question.query.filter(Question.id.in_(questions_ids)).all()

    questions_ids_db = set(question.id for question in questions)

    if questions_ids != questions_ids_db:
        raise DefaultException("question_not_found", code=404)

    return questions


def get_diagnosis(diagnosis_id: int, options: list = None) -> Diagnosis:

    query = Diagnosis.query

    if options is not None:
        query = query.options(*options)

    diagnosis = query.get(diagnosis_id)

    if diagnosis is None:
        raise DefaultException("diagnosis_not_found", code=404)

    return diagnosis


from app.main.service.protocol_service import get_protocol
