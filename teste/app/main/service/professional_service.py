from math import ceil

from sqlalchemy import func
from sqlalchemy.orm import joinedload
from werkzeug.datastructures import ImmutableMultiDict

from app.main import db
from app.main.config import Config
from app.main.exceptions import DefaultException, ValidationException
from app.main.model import Address, Occupation, Professional, ProfessionalBond
from app.main.service.custom_fields import date_from_string, datetime_from_string

from ..enum import *

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def get_professionals(params: ImmutableMultiDict):

    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)
    name = params.get("name", type=str)
    email = params.get("email", type=str)
    cpf = params.get("cpf", type=str)
    occupation_id = params.get("occupation_id", type=int)
    occupation_name = params.get("occupation_name", type=str)
    cns_cod = params.get("cns_cod", type=str)
    social_name = params.get("social_name", type=str)

    filters = [Professional.inactive == False]

    if name:
        filters.append(Professional.name.ilike(f"%{name}%"))
    if email:
        filters.append(Professional.email.ilike(f"%{email}%"))
    if cpf:
        filters.append(Professional.cpf.ilike(f"%{cpf}%"))
    if occupation_id:
        filters.append(
            Professional.professional_bonds.any(
                ProfessionalBond.occupation.has(Occupation.id == occupation_id)
            )
        )
    if occupation_name:
        filters.append(
            Professional.professional_bonds.any(
                ProfessionalBond.occupation.has(
                    Occupation.name.ilike(f"%{occupation_name}%")
                )
            )
        )
    if cns_cod:
        filters.append(Professional.cns_cod.ilike(f"%{cns_cod}%"))
    if social_name:
        filters.append(Professional.social_name.ilike(f"%{social_name}%"))

    pagination = (
        Professional.query.options(joinedload("address"))
        .filter(*filters)
        .order_by(Professional.id)
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return {
        "current_page": page,
        "total_items": pagination.total,
        "total_pages": ceil(pagination.total / per_page),
        "items": pagination.items,
    }


def get_professional_by_id(professional_id: int):
    professional = get_professional(
        professional_id=professional_id, options=[joinedload("address")]
    )

    return professional


def get_professional_by_name(professional_name: str) -> list[tuple[str, any]]:
    if len(professional_name) < 3:
        raise ValidationException(
            errors={"professional_name": "Name must be at least 3 characters long"},
            message="professional_short_name",
        )

    professionals = (
        Professional.query.with_entities(
            Professional.id, Professional.name, Professional.social_name
        )
        .filter(
            Professional.name.ilike(f"%{professional_name}%"),
            Professional.social_name.ilike(f"%{professional_name}%"),
            Professional.inactive == False,
        )
        .all()
    )

    return professionals


def save_new_professional(data: dict[str, any]):

    # Check if Email or CPF is already in use
    if (
        professional := Professional.query.with_entities(
            Professional.cpf, Professional.email
        )
        .filter(
            (Professional.cpf == data.get("cpf"))
            | (Professional.email == data.get("email"))
        )
        .first()
    ):
        if professional.cpf == data.get("cpf"):
            raise DefaultException("cpf_in_use", code=409)
        else:
            raise DefaultException("email_in_use", code=409)

    address_data = data.get("address")

    new_address = Address(
        cep=address_data.get("cep"),
        state=address_data.get("state"),
        district=address_data.get("district"),
        city=address_data.get("city"),
        number=address_data.get("number"),
        complement=address_data.get("complement"),
        street=address_data.get("street"),
    )

    new_professional = Professional(
        name=data.get("name"),
        social_name=data.get("social_name"),
        cpf=data.get("cpf"),
        cns_cod=data.get("cns_cod"),
        birth=date_from_string(value=data.get("birth")),
        breed=data.get("breed"),
        gender=data.get("gender"),
        sex=data.get("sex"),
        mother_name=data.get("mother_name"),
        father_name=data.get("father_name"),
        education=data.get("education"),
        nationality=data.get("nationality"),
        country=data.get("country"),
        FU_of_nationality=data.get("FU_of_nationality"),
        citizenship=data.get("citizenship"),
        date_of_entry=date_from_string(value=data.get("date_of_entry")),
        date_of_naturalization=date_from_string(
            value=data.get("date_of_naturalization")
        ),
        email=data.get("email"),
        ddi=data.get("ddi"),
        emergency_phone=data.get("emergency_phone"),
        bank_number=data.get("bank_number"),
        bank_name=data.get("bank_name"),
        agency_number=data.get("agency_number"),
        current_account=data.get("current_account"),
        address=new_address,
    )

    db.session.add(new_professional)
    db.session.commit()


def update_professional(professional_id: int, data: dict[str, any]) -> None:

    professional = get_professional(professional_id=professional_id)

    change_cpf = data.get("cpf") != professional.cpf
    change_email = data.get("email") != professional.email

    # Check if changed email or cpf is already in use
    if change_cpf or change_email:
        if (
            professional_db := Professional.query.with_entities(
                Professional.cpf, Professional.email
            )
            .filter(
                (Professional.id != professional_id)
                & (
                    (Professional.email == data.get("email"))
                    | (Professional.cpf == data.get("cpf"))
                )
            )
            .first()
        ):

            if change_cpf and professional_db.cpf == data.get("cpf"):
                raise DefaultException("cpf_in_use", code=409)
            else:
                raise DefaultException("email_in_use", code=409)

    if change_cpf:
        professional.cpf = data.get("cpf")

    if change_email:
        professional.email = data.get("email")

    # Update address info
    address = professional.address
    data_address = data.get("address")

    address.cep = data_address["cep"]
    address.state = data_address["state"]
    address.district = data_address["district"]
    address.city = data_address["city"]
    address.number = data_address["number"]
    address.complement = data_address["complement"]
    address.street = data_address["street"]

    # Update professional info
    professional.name = data.get("name")
    professional.social_name = data.get("social_name")
    professional.cpf = data.get("cpf")
    professional.cns_cod = data.get("cns_cod")
    professional.birth = date_from_string(value=data.get("birth"))
    professional.breed = data.get("breed")
    professional.gender = data.get("gender")
    professional.sex = data.get("sex")
    professional.mother_name = data.get("mother_name")
    professional.father_name = data.get("father_name")
    professional.education = data.get("education")
    professional.nationality = data.get("nationality")
    professional.country = data.get("country")
    professional.FU_of_nationality = data.get("FU_of_nationality")
    professional.citizenship = data.get("citizenship")
    professional.date_of_entry = date_from_string(value=data.get("date_of_entry"))
    professional.date_of_naturalization = date_from_string(
        value=data.get("date_of_naturalization")
    )
    professional.email = data.get("email")
    professional.ddi = data.get("ddi")
    professional.emergency_phone = data.get("emergency_phone")
    professional.bank_number = data.get("bank_number")
    professional.bank_name = data.get("bank_name")
    professional.agency_number = data.get("agency_number")
    professional.current_account = data.get("current_account")

    db.session.commit()


def activate_professional(professional_id: int) -> None:

    professional = get_professional(
        professional_id=professional_id, inactive_check=False
    )

    if not professional.inactive:
        raise DefaultException("professional_is_active", code=409)

    professional.inactive = False

    db.session.commit()


def inactivate_professional(professional_id: int, data: dict[str, any]) -> None:

    professional = get_professional(professional_id=professional_id)

    if professional.inactive == True:
        raise DefaultException("professional_is_inactive", code=409)

    professional.inactive = True
    professional.dismissal_cause = data.get("dismissal_cause")
    professional.inactivation_date = func.now()
    #professional.updating_professional_id = #logged professional
    
    db.session.commit()
    print('função de inativar profissional executada com sucesso')


def get_professional(
    professional_id: int, options: list = None, inactive_check: bool = True
) -> Professional:

    query = Professional.query

    if options is not None:
        query = query.options(*options)

    professional = query.get(professional_id)

    if professional is None:
        raise DefaultException("professional_not_found", code=404)

    if inactive_check and professional.inactive:
        raise DefaultException("professional_is_inactive", code=409)

    return professional
