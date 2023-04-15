from math import ceil

from werkzeug.datastructures import ImmutableMultiDict

from app.main import db
from app.main.config import Config
from app.main.exceptions import DefaultException
from app.main.model import MedicalAppointment

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def get_medical_appointment_history(params: ImmutableMultiDict, patient_id: int):

    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)

    get_patient(patient_id=patient_id)

    filters = [MedicalAppointment.patient_id == patient_id]

    pagination = (
        MedicalAppointment.query.filter(*filters)
        .order_by(MedicalAppointment.id)
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return {
        "current_page": page,
        "total_items": pagination.total,
        "total_pages": ceil(pagination.total / per_page),
        "items": pagination.items,
    }


def save_medical_appointment(data: dict[str, str]) -> None:

    patient = get_patient(patient_id=data.get("patient_id"))

    professional = get_professional(professional_id=data.get("professional_id"))

    new_medical_appointment = MedicalAppointment(
        patient=patient,
        professional=professional,
        description=data.get("description"),
        diagnosis_type=data.get("diagnosis_type"),
        diagnosis_work=data.get("diagnosis_work"),
        diagnosis_traffic_accident=data.get("diagnosis_traffic_accident"),
    )

    db.session.add(new_medical_appointment)
    db.session.commit()


def get_medical_appointment(
    medical_appointment_id: int, options: list
) -> MedicalAppointment:

    query = MedicalAppointment.query

    if options is not None:
        query = query.options(*options)

    medical_appointment = query.get(medical_appointment_id)

    if medical_appointment is None:
        raise DefaultException("medical_appointment_not_found", code=404)

    return medical_appointment


from app.main.service.patient_service import get_patient
from app.main.service.professional_service import get_professional
