from math import ceil

from werkzeug.datastructures import ImmutableMultiDict

from app.main import db
from app.main.config import Config
from app.main.exceptions import DefaultException
from app.main.model import MedicalSpecialty

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def get_medical_specialties(params: ImmutableMultiDict):

    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)
    name = params.get("name", type=str)

    filters = []

    if name:
        filters.append(MedicalSpecialty.name.ilike(f"%{name.upper()}%"))

    pagination = (
        MedicalSpecialty.query.filter(*filters)
        .order_by(MedicalSpecialty.id)
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return {
        "current_page": page,
        "total_items": pagination.total,
        "total_pages": ceil(pagination.total / per_page),
        "items": pagination.items,
    }


def save_new_medical_specialty(data: dict[str, any]) -> None:

    name = data.get("name")
    if _medical_specialty_exists(name):
        raise DefaultException("name_in_use", code=409)

    new_medical_specialty = MedicalSpecialty(name=name)

    db.session.add(new_medical_specialty)
    db.session.commit()


def update_medical_specialty(medical_specialty_id: int, data: dict[str, str]) -> None:

    medical_specialty = get_medical_specialty(medical_specialty_id=medical_specialty_id)

    new_name = data.get("name").upper()

    if medical_specialty.name != new_name and _medical_specialty_exists(new_name):
        raise DefaultException("name_in_use", code=409)

    medical_specialty.name = new_name
    db.session.add(medical_specialty)
    db.session.commit()


def delete_medical_specialty(medical_specialty_id: int):

    medical_specialty = get_medical_specialty(medical_specialty_id=medical_specialty_id)

    db.session.delete(medical_specialty)
    db.session.commit()


def get_medical_specialty(
    medical_specialty_id: int, options: list = None
) -> MedicalSpecialty:

    query = MedicalSpecialty.query

    if options is not None:
        query = query.options(*options)

    medical_specialty = query.get(medical_specialty_id)

    if medical_specialty is None:
        raise DefaultException("medical_specialty_not_found", code=404)

    return medical_specialty


def _medical_specialty_exists(medical_specialty_name: str) -> bool:
    return (
        MedicalSpecialty.query.with_entities(MedicalSpecialty.id)
        .filter(MedicalSpecialty.name == medical_specialty_name.upper())
        .scalar()
        is not None
    )
