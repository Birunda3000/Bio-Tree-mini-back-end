from math import ceil

from werkzeug.datastructures import ImmutableMultiDict

from app.main import db
from app.main.config import Config
from app.main.exceptions import DefaultException
from app.main.model import (
    MedicalPrescription,
    MedicalPrescriptionMedicine,
    MedicalPrescriptionOrientation,
    MedicalPrescriptionProcedure,
    Medicine,
    Procedure,
)

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def get_medical_prescriptions(params: ImmutableMultiDict):

    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)
    professional_id = params.get("professional_id", type=int)
    patient_id = params.get("patient_id", type=int)

    filters = []

    if professional_id is not None:
        filters.append(MedicalPrescription.professional_id == professional_id)

    if patient_id is not None:
        filters.append(MedicalPrescription.patient_id == patient_id)

    pagination = (
        MedicalPrescription.query.filter(*filters)
        .order_by(MedicalPrescription.id)
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return {
        "current_page": page,
        "total_items": pagination.total,
        "total_pages": ceil(pagination.total / per_page),
        "items": pagination.items,
    }


def get_medical_prescription_by_id(medical_prescription_id: int) -> MedicalPrescription:

    return get_medical_prescription(medical_prescription_id=medical_prescription_id)


def save_medical_prescription(data: dict[str, str]) -> None:

    medical_prescription_type = data.get("type")

    if medical_prescription_type == "Observação":
        queue_id = 3
    elif medical_prescription_type == "Internação":
        queue_id = 4

    professional = get_professional(professional_id=data.get("professional_id"))

    patient = get_patient(patient_id=data.get("patient_id"))

    room = get_room(room_id=data.get("room_id"))

    procedures_data = data.get("procedures")
    if procedures_data:
        procedures_ids = set(
            [procedure.get("procedure_id") for procedure in procedures_data]
        )
        procedures_db = Procedure.query.filter(Procedure.id.in_(procedures_ids)).all()
        procedures_ids_db = set([procedure.id for procedure in procedures_db])
        if procedures_ids != procedures_ids_db:
            raise DefaultException("medical_prescription_procedure_not_found", code=404)

    medicines_data = data.get("medicines")

    if medicines_data:
        medicines_ids = set(
            [medicine.get("medicine_id") for medicine in medicines_data]
        )
        medicines_db = Medicine.query.filter(Medicine.id.in_(medicines_ids)).all()
        medicines_ids_db = set([medicine.id for medicine in medicines_db])
        if medicines_ids != medicines_ids_db:
            raise DefaultException("medical_prescription_medicine_not_found", code=404)

    new_medical_prescription = MedicalPrescription(
        professional=professional, patient=patient, room=room
    )

    orientations_data = data.get("orientations")
    if orientations_data:
        orientations = []

        for orientation in orientations_data:
            new_orientation = MedicalPrescriptionOrientation(
                medical_prescription=new_medical_prescription,
                orientation=orientation.get("orientation"),
                execute_at=datetime_from_string(orientation.get("execute_at")),
                observations=orientation.get("observations"),
            )
            orientations.append(new_orientation)

        db.session.add_all(orientations)

    medicines_data = data.get("medicines")
    if medicines_data:
        medicines = []

        for medicine in medicines_data:
            new_medicine = MedicalPrescriptionMedicine(
                medical_prescription=new_medical_prescription,
                medicine_id=medicine.get("medicine_id"),
                execute_at=datetime_from_string(medicine.get("execute_at")),
                observations=medicine.get("observations"),
            )
            medicines.append(new_medicine)

        db.session.add_all(medicines)

    procedures_data = data.get("procedures")
    if procedures_data:
        procedures = []

        for procedure in procedures_data:
            new_procedure = MedicalPrescriptionProcedure(
                medical_prescription=new_medical_prescription,
                procedure_id=procedure.get("procedure_id"),
                execute_at=datetime_from_string(procedure.get("execute_at")),
                observations=procedure.get("observations"),
            )
            procedures.append(new_procedure)

        db.session.add_all(procedures)

    change_patient_queue({"patient_id": patient.id, "queue_id": queue_id})

    db.session.add(new_medical_prescription)
    db.session.commit()


def get_medical_prescription(
    medical_prescription_id: int, options: list = None
) -> MedicalPrescription:

    query = MedicalPrescription.query

    if options is not None:
        query = query.options(*options)

    medical_prescription = query.get(medical_prescription_id)

    if medical_prescription is None:
        raise DefaultException("medical_prescription_not_found", code=404)

    return medical_prescription


from app.main.service.custom_fields import datetime_from_string
from app.main.service.patient_service import get_patient
from app.main.service.professional_service import get_professional
from app.main.service.queue_manager_service import change_patient_queue
from app.main.service.room_service import get_room
