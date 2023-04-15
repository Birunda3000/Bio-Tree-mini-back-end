from math import ceil

from sqlalchemy.orm import joinedload
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.datastructures import ImmutableMultiDict

from app.main import db
from app.main.config import Config
from app.main.exceptions.default_exception import DefaultException
from app.main.model import QueueManager, Vaccine, VaccineApplicationRequest

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def get_vaccine_application_requests(params: ImmutableMultiDict):
    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)
    professional_name = params.get("professional_name", type=str)
    patient_id = params.get("patient_id", type=int)
    patient_name = params.get("patient_name", type=str)
    vaccine_name = params.get("vaccine_name", type=str)
    status = params.get("status", type=str)

    filters = []

    if professional_name:
        filters.append(
            VaccineApplicationRequest.professional.has(
                professional_name_filter(professional_name=professional_name)
            )
        )
    if patient_id:
        filters.append(VaccineApplicationRequest.patient_id == patient_id)
    if patient_name:
        filters.append(
            VaccineApplicationRequest.patient.has(
                patient_name_filter(patient_name=patient_name)
            )
        )
    if vaccine_name:
        filters.append(
            VaccineApplicationRequest.vaccine.has(
                Vaccine.name.ilike(f"%{vaccine_name}%")
            )
        )
    if status:
        filters.append(VaccineApplicationRequest.status == status)

    pagination = (
        VaccineApplicationRequest.query.options(
            joinedload("professional").load_only("name", "social_name"),
            joinedload("patient").load_only("name", "social_name"),
            joinedload("vaccine").load_only("name"),
        )
        .filter(*filters)
        .order_by(VaccineApplicationRequest.id)
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return {
        "current_page": page,
        "total_items": pagination.total,
        "total_pages": ceil(pagination.total / per_page),
        "items": pagination.items,
    }


def save_new_vaccine_application_request(data: dict[str, any]) -> None:
    professional_id = data.get("professional_id")
    patient_id = data.get("patient_id")
    vaccine_id = data.get("vaccine_id")
    patient = get_patient(patient_id=patient_id)
    professional = get_professional(professional_id=professional_id)
    vaccine = get_vaccine(vaccine_id=vaccine_id)

    _validate_vaccine_application_request_relationships(patient_id=patient_id)

    new_vaccine_application_request = VaccineApplicationRequest(
        professional=professional,
        patient=patient,
        vaccine=vaccine,
    )

    db.session.add(new_vaccine_application_request)
    db.session.commit()


def update_vaccine_application_request(vaccine_application_request_id: int) -> None:

    vaccine_application = get_vaccine_application_request(
        vaccine_application_request_id=vaccine_application_request_id
    )

    if vaccine_application.status != "Em aguardo":
        raise DefaultException("vaccine_application_request_already_canceled", code=409)

    vaccine_application.status = "Cancelada"

    db.session.commit()


def get_vaccine_application_request(
    vaccine_application_request_id: int, options: list = None
) -> VaccineApplicationRequest:

    filters = [VaccineApplicationRequest.id == vaccine_application_request_id]

    query = VaccineApplicationRequest.query.filter(*filters)

    if options is not None:
        query = query.options(*options)

    try:
        vaccine_application_request = query.one()
    except NoResultFound:
        raise DefaultException("vaccine_application_request_not_found", code=404)

    return vaccine_application_request


def _validate_vaccine_application_request_relationships(patient_id: int):

    queue_manager = (
        QueueManager.query.options(joinedload("risk_classification"))
        .filter(
            QueueManager.patient_id == patient_id, QueueManager.hospital_exit.is_(None)
        )
        .first()
    )

    if not queue_manager:
        raise DefaultException("queue_manager_not_found", code=404)

    if not queue_manager.risk_classification:
        raise DefaultException("risk_classification_not_found", code=404)


from app.main.service.filters_service import (
    patient_name_filter,
    professional_name_filter,
)
from app.main.service.patient_service import get_patient
from app.main.service.professional_service import get_professional
from app.main.service.vaccine.vaccine_service import get_vaccine
