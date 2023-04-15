from math import ceil

from sqlalchemy import and_, or_
from sqlalchemy.orm import joinedload
from werkzeug.datastructures import ImmutableMultiDict

from app.main import db
from app.main.config import Config
from app.main.exceptions import DefaultException, ValidationException
from app.main.model import CompanyAddress, Contact, Fces

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def get_fcess(params: ImmutableMultiDict):

    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)
    commercial_name = params.get("commercial_name", type=str)

    filters = []

    if commercial_name:
        filters.append(Fces.commercial_name.ilike(f"%{commercial_name}%"))

    pagination = (
        Fces.query.options(
            joinedload("maintainer"),
            joinedload("professional"),
            joinedload("company_address"),
            joinedload("contact"),
        )
        .filter(*filters)
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return {
        "current_page": page,
        "total_items": pagination.total,
        "total_pages": ceil(pagination.total / per_page),
        "items": pagination.items,
    }


def save_new_fces(data: dict[str, any]):

    person_type = data.get("person_type")
    cnpj = data.get("cnpj")
    cpf = data.get("cpf")

    _valid_person_type(
        data_person_type=person_type,
        data_cnpj=cnpj,
        data_cpf=cpf,
    )

    corporate_name = data.get("corporate_name")
    cnes_code = data.get("cnes_code")

    email = data.get("email")

    filters = [
        or_(
            Fces.corporate_name == corporate_name,
            Fces.cnes_code == cnes_code,
            Fces.email == email,
            and_(Fces.cnpj == cnpj, Fces.cnpj != None),
            and_(Fces.cpf == cpf, Fces.cpf != None),
        )
    ]

    if (
        fces := Fces.query.with_entities(
            Fces.corporate_name, Fces.cnes_code, Fces.cnpj, Fces.cpf, Fces.email
        )
        .filter(*filters)
        .first()
    ):
        if fces.corporate_name == corporate_name:
            raise DefaultException("corporate_name_in_use", code=409)
        elif fces.cnes_code == cnes_code:
            raise DefaultException("cnes_code_in_use", code=409)
        elif fces.email == email:
            raise DefaultException("email_in_use", code=409)
        elif (cnpj is not None) and (fces.cnpj == cnpj):
            raise DefaultException("cnpj_in_use", code=409)
        elif (cpf is not None) and (fces.cpf == cpf):
            raise DefaultException("cpf_in_use", code=409)

    maintainer = get_maintainer(maintainer_id=data.get("maintainer_id"))

    professional = get_professional(professional_id=data.get("professional_id"))

    address_data = data.get("company_address")
    sanitary_district_id = address_data.get("sanitary_district_id")

    sanitary_district = get_sanitary_district(sanitary_district_id=sanitary_district_id)

    new_address = CompanyAddress(
        street=address_data.get("street"),
        district=address_data.get("district"),
        city=address_data.get("city"),
        state=address_data.get("state"),
        complement=address_data.get("complement"),
        number=address_data.get("number"),
        cep=address_data.get("cep"),
        municipality=address_data.get("municipality"),
        latitude=address_data.get("latitude"),
        longitude=address_data.get("longitude"),
        regional_health=address_data.get("regional_health"),
        microregion=address_data.get("microregion"),
        assistance_module=address_data.get("assistance_module"),
        sanitary_district=sanitary_district,
    )

    contact_data = data.get("contact")

    new_contact = Contact(phone=contact_data.get("phone"), fax=contact_data.get("fax"))

    new_fces = Fces(
        corporate_name=data.get("corporate_name"),
        commercial_name=data.get("commercial_name"),
        cnes_code=data.get("cnes_code"),
        person_type=data.get("person_type"),
        cnpj=cnpj,
        cpf=cpf,
        email=email,
        establishment_code=data.get("establishment_code"),
        situation=data.get("situation"),
        establishment_type=data.get("establishment_type"),
        establishment_subtype=data.get("establishment_subtype"),
        regulatory_registration_end_date=data.get("regulatory_registration_end_date"),
        payment_to_provider=data.get("payment_to_provider"),
        maintainer=maintainer,
        professional=professional,
        company_address=new_address,
        contact=new_contact,
    )

    db.session.add(new_fces)
    db.session.commit()


def update_fces(fces_id: int, data: dict[str, any]) -> None:

    fces = get_fces(fces_id=fces_id)

    email = data.get("email")
    corporate_name = data.get("corporate_name")

    change_email = email != fces.email
    change_corporate_name = corporate_name != fces.corporate_name

    if change_corporate_name or change_email:

        filters = [
            and_(
                Fces.id != fces_id,
                or_(Fces.corporate_name == corporate_name, Fces.email == email),
            )
        ]

        if (
            fces_db := Fces.query.with_entities(Fces.corporate_name, Fces.email)
            .filter(*filters)
            .first()
        ):
            if fces_db.corporate_name == corporate_name:
                raise DefaultException("corporate_name_in_use", code=409)
            else:
                raise DefaultException("email_in_use", code=409)

    maintainer_id = data.get("maintainer_id")
    professional_id = data.get("professional_id")

    if fces.maintainer_id != maintainer_id:
        fces.maintainer = get_maintainer(maintainer_id=maintainer_id)

    if fces.professional_id != professional_id:
        fces.professional = get_professional(professional_id=professional_id)

    address = fces.company_address
    data_address = data.get("company_address")
    sanitary_district_id = data_address.get("sanitary_district_id")

    if address.sanitary_district_id != sanitary_district_id:
        address.sanitary_district = get_sanitary_district(
            sanitary_district_id=sanitary_district_id
        )

    address.street = data_address.get("street")
    address.district = data_address.get("district")
    address.city = data_address.get("city")
    address.state = data_address.get("state")
    address.complement = data_address.get("complement")
    address.number = data_address.get("number")
    address.cep = data_address.get("cep")
    address.municipality = data_address.get("municipality")
    address.latitude = data_address.get("latitude")
    address.longitude = data_address.get("longitude")
    address.regional_health = data_address.get("regional_health")
    address.microregion = data_address.get("microregion")
    address.assistance_module = data_address.get("assistance_module")

    contact = fces.contact
    data_contact = data.get("contact")

    contact.phone = data_contact.get("phone")
    contact.fax = data_contact.get("fax")

    fces.corporate_name = corporate_name
    fces.commercial_name = data.get("commercial_name")
    fces.email = email
    fces.establishment_code = data.get("establishment_code")
    fces.situation = data.get("situation")
    fces.establishment_type = data.get("establishment_type")
    fces.establishment_subtype = data.get("establishment_subtype")
    fces.regulatory_registration_end_date = data.get("regulatory_registration_end_date")
    fces.payment_to_provider = data.get("payment_to_provider")

    db.session.commit()


def get_fces(fces_id: int, options: list = None) -> Fces:

    query = Fces.query

    if options is not None:
        query = query.options(*options)

    fces = query.get(fces_id)

    if fces is None:
        raise DefaultException("fces_not_found", code=404)

    return fces


def _valid_person_type(data_person_type: str, data_cnpj: str, data_cpf: str):
    if data_cnpj and data_cpf:
        raise ValidationException(
            errors={"cnpj_cpf": "cnpj and cpf sent simultaneously"},
            message="cnpj_cpf_sent_simultaneously",
        )
    elif data_person_type == "Jurídica":
        if not data_cnpj:
            raise ValidationException(
                errors={"cnpj": "register_without_cnpj"},
                message="Input payload validation failed",
            )
    elif data_person_type == "Física":
        if not data_cpf:
            raise ValidationException(
                errors={"cpf": "register_without_cpf"},
                message="Input payload validation failed",
            )


from app.main.service import get_professional
from app.main.service.maintainer_service import get_maintainer
from app.main.service.sanitary_district_service import get_sanitary_district
