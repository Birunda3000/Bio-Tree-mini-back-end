from math import ceil

from sqlalchemy.orm import joinedload
from werkzeug.datastructures import ImmutableMultiDict

from app.main import db
from app.main.config import Config
from app.main.exceptions import DefaultException
from app.main.model import Admission

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def get_admissions(params: ImmutableMultiDict):
    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)
    patient_id = params.get("patient_id", type=int)
    professional_id = params.get("professional_id", type=int)
    bed_id = params.get("bed_id", type=int)

    filters = []

    if patient_id:
        filters.append(Admission.patient_id == patient_id)
    if professional_id:
        filters.append(Admission.professional_id == professional_id)
    if bed_id:
        filters.append(Admission.bed_id == bed_id)

    pagination = (
        Admission.query.options(joinedload("bed"))
        .filter(*filters)
        .order_by(Admission.id)
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return {
        "current_page": page,
        "total_items": pagination.total,
        "total_pages": ceil(pagination.total / per_page),
        "items": pagination.items,
    }


def save_new_admission(data: dict[str, any]) -> None:
    patient_id = data.get("patient_id")
    professional_id = data.get("professional_id")
    bed_id = data.get("bed_id")
    admission_type = data.get("type")

    patient = get_patient(patient_id=patient_id)

    if admission_type == "Observação":
        queue_id = 3
    elif admission_type == "Internação":
        queue_id = 4

    if not is_patient_in_queue(patient_id=patient.id, queue_id=queue_id):
        raise DefaultException("patient_not_in_queue", code=409)

    professional = get_professional(professional_id=professional_id)

    bed = get_bed(bed_id=bed_id)

    new_admission = Admission(
        patient=patient,
        professional=professional,
        bed=bed,
        type=admission_type,
    )

    bed.available = False

    db.session.add(new_admission)
    db.session.commit()


def get_admission(admission_id: int, options: list = None) -> Admission:

    query = Admission.query

    if options is not None:
        query = query.options(*options)

    admission = query.get(admission_id)

    if admission is None:
        raise DefaultException("admission_not_found", code=404)

    return admission


from app.main.service.bed.bed_service import get_bed
from app.main.service.patient_service import get_patient
from app.main.service.professional_service import get_professional
from app.main.service.queue_manager_service import is_patient_in_queue
