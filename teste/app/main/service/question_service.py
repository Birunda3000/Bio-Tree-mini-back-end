from math import ceil

from werkzeug.datastructures import ImmutableMultiDict

from app.main import db
from app.main.config import Config
from app.main.exceptions import DefaultException
from app.main.model import Question

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def get_questions(params: ImmutableMultiDict):
    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)
    name = params.get("name", type=str)

    filters = []

    if name:
        filters.append(Question.name.ilike(f"%{name.upper()}"))

    pagination = (
        Question.query.filter(*filters)
        .order_by(Question.id)
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return {
        "current_page": page,
        "total_items": pagination.total,
        "total_pages": ceil(pagination.total / per_page),
        "items": pagination.items,
    }


def get_question_by_id(question_id):
    return get_question(question_id=question_id)


def save_new_question(data: dict[str, any]):

    name = data.get("name")

    question = Question.query.filter((Question.name == name.upper())).first()

    if question:
        raise DefaultException("name_in_use", code=409)

    new_question = Question(name=name)

    db.session.add(new_question)
    db.session.commit()


def update_question(question_id: int, data: dict[str, any]) -> None:

    question = get_question(question_id=question_id)
    name = data.get("name").upper()

    change_question = Question.query.filter((Question.name == name)).first()

    if change_question:
        raise DefaultException("name_in_use", code=409)

    question.name = name

    db.session.commit()


def delete_question(question_id: int) -> None:
    question = get_question(question_id=question_id)

    if question.diagnoses:
        raise DefaultException("question_is_associated_with_diagnosis", code=409)

    db.session.delete(question)
    db.session.commit()


def get_question(question_id: int, options: list = None) -> Question:

    query = Question.query

    if options is not None:
        query = query.options(*options)

    question = query.get(question_id)

    if question is None:
        raise DefaultException("question_not_found", code=404)

    return question
