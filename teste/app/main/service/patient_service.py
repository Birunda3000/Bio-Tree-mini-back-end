from math import ceil

from sqlalchemy.orm import joinedload
from werkzeug.datastructures import ImmutableMultiDict

from app.main import db
from app.main.config import Config
from app.main.exceptions import DefaultException, ValidationException
from app.main.model import Address, Contact, Patient

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def get_patients(params: ImmutableMultiDict):

    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)
    name = params.get("name", type=str)
    cpf = params.get("cpf", type=str)
    cns_cod = params.get("cns_cod", type=str)
    social_name = params.get("social_name", type=str)
    mother_name = params.get("mother_name", type=str)

    filters = []

    if name:
        filters.append(Patient.name.ilike(f"%{name}%"))
    if cpf:
        filters.append(Patient.cpf.ilike(f"%{cpf}%"))
    if cns_cod:
        filters.append(Patient.cns_cod.ilike(f"%{cns_cod}%"))
    if social_name:
        filters.append(Patient.social_name.ilike(f"%{social_name}%"))
    if mother_name:
        filters.append(Patient.mother_name.ilike(f"%{mother_name}%"))

    pagination = (
        Patient.query.options(joinedload("address"), joinedload("contact"))
        .filter(*filters)
        .order_by(Patient.id)
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return {
        "current_page": page,
        "total_items": pagination.total,
        "total_pages": ceil(pagination.total / per_page),
        "items": pagination.items,
    }


def get_patient_by_id(patient_id):
    patient = get_patient(
        patient_id=patient_id, options=[joinedload("address"), joinedload("contact")]
    )

    return patient


def get_patient_by_name(patient_name: str) -> list[tuple[str, any]]:
    if len(patient_name) < 3:
        raise ValidationException(
            errors={"patient_name": "Name must be at least 1 characters long"},
            message="patient_short_name",
        )

    patients = (
        Patient.query.with_entities(Patient.id, Patient.name)
        .filter(Patient.name.ilike(f"%{patient_name}%"))
        .all()
    )

    return patients


def save_new_patient(data: dict[str, any]):

    cpf = data.get("cpf")
    email = data.get("email")
    birth = data.get("birth")

    filters = [(Patient.cpf == cpf) | (Patient.email == email)]

    if (
        patient := Patient.query.with_entities(Patient.cpf, Patient.email)
        .filter(*filters)
        .first()
    ):
        if patient.cpf == cpf:
            raise DefaultException("cpf_in_use", code=409)
        else:
            raise DefaultException("email_in_use", code=409)

    address_data = data.get("address")

    new_address = Address(
        street=address_data.get("street"),
        district=address_data.get("district"),
        city=address_data.get("city"),
        state=address_data.get("state"),
        complement=address_data.get("complement"),
        number=address_data.get("number"),
        cep=address_data.get("cep"),
    )

    new_patient = Patient(
        name=data.get("name"),
        cpf=cpf,
        email=email,
        birth=date_from_string(birth),
        sex=data.get("sex"),
        mother_name=data.get("mother_name"),
        cns_cod=data.get("cns_cod"),
        gender=data.get("gender"),
        medical_number=data.get("medical_number"),
        breed=data.get("breed"),
        address=new_address,
        social_name=data.get("social_name"),
        father_name=data.get("father_name"),
    )

    contact_data = data.get("contact")

    if contact_data is not None:
        new_contact = Contact(
            phone=contact_data.get("phone"),
            cellphone=contact_data.get("cellphone"),
            emergency_contact=contact_data.get("emergency_contact"),
        )
        new_patient.contact = new_contact

    db.session.add(new_patient)
    db.session.commit()


def update_patient(patient_id: int, data: dict[str, any]) -> None:

    patient = get_patient(patient_id=patient_id)
    cpf = data.get("cpf")
    email = data.get("email")

    change_cpf = cpf != patient.cpf
    change_email = email != patient.email

    if change_cpf or change_email:

        filters = [
            (Patient.id != patient_id)
            & ((Patient.email == email) | (Patient.cpf == cpf))
        ]

        if (
            patient_db := Patient.query.with_entities(Patient.cpf, Patient.email)
            .filter(*filters)
            .first()
        ):
            if change_cpf and patient_db.cpf == data.get("cpf"):
                raise DefaultException("cpf_in_use", code=409)
            else:
                raise DefaultException("email_in_use", code=409)

    if change_cpf:
        patient.cpf = data.get("cpf")

    if change_email:
        patient.email = data.get("email")

    if data.get("cpf") != patient.cpf:
        exists_by_cpf = Patient.query.filter_by(cpf=data.get("cpf")).scalar()

        if exists_by_cpf:
            raise DefaultException("cpf_in_use", code=409)

    address = patient.address
    data_address = data.get("address")

    address.street = data_address.get("street")
    address.district = data_address.get("district")
    address.city = data_address.get("city")
    address.state = data_address.get("state")
    address.complement = data_address.get("complement")
    address.number = data_address.get("number")
    address.cep = data_address.get("cep")

    contact_data = data.get("contact")

    if contact_data is not None:
        contact = patient.contact
        contact.phone = contact_data.get("phone")
        contact.cellphone = contact_data.get("cellphone")
        contact.emergency_contact = contact_data.get("emergency_contact")

    patient.name = data.get("name")
    patient.cpf = data.get("cpf")
    patient.phone = data.get("phone")
    patient.cellphone = data.get("cellphone")
    patient.email = data.get("email")
    patient.emergency_contact = data.get("emergency_contact")
    patient.birth = date_from_string(data.get("birth"))
    patient.sex = data.get("sex")
    patient.mother_name = data.get("mother_name")
    patient.cns_cod = data.get("cns_cod")
    patient.gender = data.get("gender")
    patient.medical_number = data.get("medical_number")
    patient.breed = data.get("breed")
    patient.social_name = data.get("social_name")
    patient.father_name = data.get("father_name")

    db.session.commit()


def get_patient(patient_id: int, options: list = None) -> Patient:

    query = Patient.query

    if options is not None:
        query = query.options(*options)

    patient = query.get(patient_id)

    if patient is None:
        raise DefaultException("patient_not_found", code=404)

    return patient


from app.main.service.custom_fields import date_from_string
