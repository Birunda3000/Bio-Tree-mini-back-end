from math import ceil

from sqlalchemy import func
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.datastructures import ImmutableMultiDict

from app.main import db
from app.main.config import Config
from app.main.exceptions.default_exception import DefaultException
from app.main.model import Patient, QueueManager, VaccineApplication

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def get_vaccine_applications(params: ImmutableMultiDict):
    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)
    professional_id = params.get("professional_id", type=int)
    professional_name = params.get("professional_name", type=str)
    patient_id = params.get("patient_id", type=int)
    patient_name = params.get("patient_name", type=str)
    patient_mother_name = params.get("patient_mother_name", type=str)
    vaccine_name = params.get("vaccine_name", type=str)
    performed_at = params.get("performed_at", type=str)

    filters = [VaccineApplication.edited == False]

    if professional_id:
        filters.append(VaccineApplication.professional_id == professional_id)
    if professional_name:
        filters.append(
            VaccineApplication.professional.has(
                professional_name_filter(professional_name=professional_name)
            )
        )
    if patient_id:
        filters.append(VaccineApplication.patient_id == patient_id)
    if patient_name:
        filters.append(
            VaccineApplication.patient.has(
                patient_name_filter(patient_name=patient_name)
            )
        )
    if patient_mother_name:
        filters.append(
            VaccineApplication.patient.has(
                Patient.mother_name.ilike(f"%{patient_mother_name}%")
            )
        )
    if vaccine_name:
        filters.append(VaccineApplication.vaccine_name.ilike(f"%{vaccine_name}%"))
    if performed_at:
        filters.append(
            func.date(VaccineApplication.performed_at) == date_from_string(performed_at)
        )

    pagination = (
        VaccineApplication.query.options(
            joinedload("patient").load_only("name", "social_name", "mother_name")
        )
        .filter(*filters)
        .order_by(VaccineApplication.id)
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return {
        "current_page": page,
        "total_items": pagination.total,
        "total_pages": ceil(pagination.total / per_page),
        "items": pagination.items,
    }


def save_new_vaccine_application(data: dict[str, any]) -> None:
    patient_id = data.get("patient_id")
    professional_id = data.get("professional_id")
    patient = get_patient(patient_id=patient_id)
    professional = get_professional(professional_id=professional_id)
    application_type = data.get("application_type")

    _validate_vaccine_application_relationships(patient_id=patient_id)

    request = None

    if application_type == "Aplicação":
        request = get_vaccine_application_request(
            vaccine_application_request_id=data.get("request_id")
        )

        if request.status != "Em aguardo":
            raise DefaultException("vaccine_application_request_invalid", code=409)

        request.status = "Realizada"

    new_vaccine_application = VaccineApplication(
        professional=professional,
        patient=patient,
        request=request,
        vaccine_name=data.get("vaccine_name"),
        application_type=application_type,
        batch=data.get("batch"),
        manufacturer=data.get("manufacturer"),
        administration_route=data.get("administration_route"),
        application_site=data.get("application_site"),
        bottle_type=data.get("bottle_type"),
        bottle_doses_number=data.get("bottle_doses_number"),
        pregnancy_type=data.get("pregnancy_type"),
        complement=data.get("complement"),
        performed_at=date_from_string(
            data.get("performed_at"),
        ),
    )

    db.session.add(new_vaccine_application)
    db.session.commit()


def get_vaccine_application(
    vaccine_application_id: int, options: list = None
) -> VaccineApplication:

    filters = [VaccineApplication.id == vaccine_application_id]

    query = VaccineApplication.query.filter(*filters)

    if options is not None:
        query = query.options(*options)

    try:
        vaccine_application = query.one()
    except NoResultFound:
        raise DefaultException("vaccine_application_not_found", code=404)

    return vaccine_application


def _validate_vaccine_application_relationships(patient_id: int):

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

    if queue_manager.queue_id != 5:
        raise DefaultException("patient_not_in_vaccination_queue", code=409)


from app.main.service.custom_fields import date_from_string
from app.main.service.filters_service import (
    patient_name_filter,
    professional_name_filter,
)
from app.main.service.patient_service import get_patient
from app.main.service.professional_service import get_professional
from app.main.service.vaccine_application.vaccine_application_request_service import (
    get_vaccine_application_request,
)
