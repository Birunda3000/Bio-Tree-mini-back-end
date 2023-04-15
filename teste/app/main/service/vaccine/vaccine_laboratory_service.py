from math import ceil

from sqlalchemy import or_
from werkzeug.datastructures import ImmutableMultiDict

from app.main import db
from app.main.config import Config
from app.main.exceptions.default_exception import DefaultException
from app.main.model import VaccineLaboratory

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def get_vaccine_laboratories(params: ImmutableMultiDict):
    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)
    name = params.get("name", type=str)

    filters = []

    if name:
        filters.append(VaccineLaboratory.name.ilike(f"%{name.upper()}%"))

    pagination = (
        VaccineLaboratory.query.filter(*filters)
        .order_by(VaccineLaboratory.id)
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return {
        "current_page": page,
        "total_items": pagination.total,
        "total_pages": ceil(pagination.total / per_page),
        "items": pagination.items,
    }


def save_new_vaccine_laboratory(data: dict[str, str]) -> None:
    name = data.get("name")
    cnpj = data.get("cnpj")
    pni_code = data.get("pni_code")

    filters = [
        VaccineLaboratory.name == name.upper(),
        VaccineLaboratory.pni_code == pni_code,
    ]

    if cnpj:
        filters.append(VaccineLaboratory.cnpj == cnpj)

    filters = [or_(*filters)]

    _check_if_laboratory_already_exists(
        filters=filters, name=name.upper(), pni_code=pni_code
    )

    new_vaccine_laboratory = VaccineLaboratory(name=name, pni_code=pni_code, cnpj=cnpj)

    db.session.add(new_vaccine_laboratory)
    db.session.commit()


def update_vaccine_laboratory(vaccine_laboratory_id: int, data: dict[str, str]) -> None:
    name = data.get("name").upper()
    pni_code = data.get("pni_code")
    cnpj = data.get("cnpj")

    vaccine_laboratory = get_vaccine_laboratory(
        vaccine_laboratory_id=vaccine_laboratory_id
    )

    filters = []

    if change_name := vaccine_laboratory.name != name:
        filters.append(VaccineLaboratory.name == name)

    if change_pni_code := vaccine_laboratory.pni_code != pni_code:
        filters.append(VaccineLaboratory.pni_code == pni_code)

    change_cnpj = vaccine_laboratory.cnpj != cnpj
    if cnpj and change_cnpj:
        filters.append(VaccineLaboratory.cnpj == cnpj)

    if change_name or change_pni_code or change_cnpj:
        filters = [VaccineLaboratory.id != vaccine_laboratory.id, or_(*filters)]
        _check_if_laboratory_already_exists(
            filters=filters,
            name=name.upper(),
            pni_code=pni_code,
        )

    vaccine_laboratory.name = name
    vaccine_laboratory.pni_code = pni_code
    vaccine_laboratory.cnpj = cnpj

    db.session.commit()


def get_vaccine_laboratory(
    vaccine_laboratory_id: int, options: list = None
) -> VaccineLaboratory:
    query = VaccineLaboratory.query

    if options is not None:
        query = query.options(*options)

    vaccine_laboratory = query.get(vaccine_laboratory_id)

    if vaccine_laboratory is None:
        raise DefaultException("vaccine_laboratory_not_found", code=404)

    return vaccine_laboratory


def _check_if_laboratory_already_exists(
    filters: list[any], name: str, pni_code: str
) -> None:
    if (
        vaccine_laboratory_db := VaccineLaboratory.query.with_entities(
            VaccineLaboratory.name,
            VaccineLaboratory.pni_code,
            VaccineLaboratory.cnpj,
        )
        .filter(*filters)
        .first()
    ):
        if vaccine_laboratory_db.name == name:
            raise DefaultException("name_in_use", code=409)
        elif vaccine_laboratory_db.pni_code == pni_code:
            raise DefaultException("pni_code_in_use", code=409)
        else:
            raise DefaultException("cnpj_in_use", code=409)
