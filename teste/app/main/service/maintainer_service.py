from math import ceil

from sqlalchemy.orm import joinedload
from werkzeug.datastructures import ImmutableMultiDict

from app.main import db
from app.main.config import Config
from app.main.exceptions import DefaultException
from app.main.model import Address, Contact, Maintainer

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def get_maintainers(params: ImmutableMultiDict):

    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)
    commercial_name = params.get("commercial_name", type=str)

    filters = []

    if commercial_name:
        filters.append(Maintainer.commercial_name.ilike(f"%{commercial_name}%"))

    pagination = (
        Maintainer.query.options(joinedload("address"), joinedload("contact"))
        .filter(*filters)
        .order_by(Maintainer.commercial_name)
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return {
        "current_page": page,
        "total_items": pagination.total,
        "total_pages": ceil(pagination.total / per_page),
        "items": pagination.items,
    }


def save_new_maintainer(data: dict[str, any]):

    cnpj = data.get("cnpj")
    email = data.get("email")

    filters = [(Maintainer.cnpj == cnpj) | (Maintainer.email == email)]

    if (
        maintainer := Maintainer.query.with_entities(Maintainer.cnpj, Maintainer.email)
        .filter(*filters)
        .first()
    ):
        if maintainer.cnpj == cnpj:
            raise DefaultException("cnpj_in_use", code=409)
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

    new_maintainer = Maintainer(
        corporate_name=data.get("corporate_name"),
        commercial_name=data.get("commercial_name"),
        cnpj=data.get("cnpj"),
        regional_number=data.get("regional_number"),
        unit_type=data.get("unit_type"),
        email=email,
        address=new_address,
    )

    contact_data = data.get("contact")

    if contact_data is not None:
        new_contact = Contact(
            phone=contact_data.get("phone"),
            fax=contact_data.get("fax"),
        )
        new_maintainer.contact = new_contact

    db.session.add(new_maintainer)
    db.session.commit()


def update_maintainer(maintainer_id: int, data: dict[str, any]) -> None:

    maintainer = get_maintainer(maintainer_id=maintainer_id)
    cnpj = data.get("cnpj")
    email = data.get("email")

    change_cnpj = cnpj != maintainer.cnpj
    change_email = email != maintainer.email

    if change_cnpj or change_email:

        filters = [
            (Maintainer.id != maintainer_id)
            & ((Maintainer.email == email) | (Maintainer.cnpj == cnpj))
        ]

        if (
            maintainer_db := Maintainer.query.with_entities(
                Maintainer.cnpj, Maintainer.email
            )
            .filter(*filters)
            .first()
        ):
            if change_cnpj and maintainer_db.cnpj == data.get("cnpj"):
                raise DefaultException("cnpj_in_use", code=409)
            else:
                raise DefaultException("email_in_use", code=409)

    if change_cnpj:
        maintainer.cnpj = data.get("cnpj")

    if change_email:
        maintainer.email = data.get("email")

    if data.get("cnpj") != maintainer.cnpj:
        exists_by_cnpj = Maintainer.query.filter_by(cnpj=data.get("cnpj")).scalar()

        if exists_by_cnpj:
            raise DefaultException("cnpj_in_use", code=409)

    address = maintainer.address
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
        contact = maintainer.contact
        contact.phone = contact_data.get("phone")
        contact.cellphone = contact_data.get("cellphone")
        contact.emergency_contact = contact_data.get("emergency_contact")

    maintainer.corporate_name = data.get("corporate_name")
    maintainer.commercial_name = data.get("commercial_name")
    maintainer.cnpj = data.get("cnpj")
    maintainer.regional_number = data.get("regional_number")
    maintainer.unit_type = data.get("unit_type")
    maintainer.email = data.get("email")

    db.session.commit()


def get_maintainer(maintainer_id: int, options: list = None) -> Maintainer:

    query = Maintainer.query

    if options is not None:
        query = query.options(*options)

    maintainer = query.get(maintainer_id)

    if maintainer is None:
        raise DefaultException("maintainer_not_found", code=404)

    return maintainer
