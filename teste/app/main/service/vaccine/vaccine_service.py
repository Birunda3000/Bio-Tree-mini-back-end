from math import ceil

from sqlalchemy import or_
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from werkzeug.datastructures import ImmutableMultiDict

from app.main import db
from app.main.config import Config
from app.main.exceptions import DefaultException, ValidationException
from app.main.model import Vaccine, VaccineLaboratory

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def get_vaccines(params: ImmutableMultiDict):
    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)
    name = params.get("name", type=str)

    filters = []

    if name:
        filters.append(Vaccine.name.ilike(f"%{name.upper()}%"))

    pagination = (
        Vaccine.query.with_entities(Vaccine.id, Vaccine.name)
        .filter(*filters)
        .order_by(Vaccine.id)
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return {
        "current_page": page,
        "total_items": pagination.total,
        "total_pages": ceil(pagination.total / per_page),
        "items": pagination.items,
    }


def save_new_vaccine(data: dict[str, any]):
    name = data.get("name")

    if Vaccine.query.filter_by(name=name.upper()).first() is not None:
        raise DefaultException("vaccine_already_exists", code=409)

    laboratory_ids = set(data.get("laboratory_ids"))
    laboratories = _get_laboratories_and(laboratory_ids=laboratory_ids)

    new_vaccine = Vaccine(
        name=name,
        pni_code=data.get("pni_code"),
        belongs_to_vaccine_card=data.get("belongs_to_vaccine_card"),
        current=data.get("current"),
        export_to_esus=data.get("export_to_esus"),
        controls_vaccine_batch=data.get("controls_vaccine_batch"),
        oblige_establishment=data.get("oblige_establishment"),
        laboratories=laboratories,
    )

    db.session.add(new_vaccine)
    db.session.commit()


def update_vaccine(vaccine_id: int, data: dict[str, any]):
    name = data.get("name").upper()

    filters = [
        or_(
            Vaccine.id == vaccine_id,
            Vaccine.name == name,
        )
    ]

    try:
        vaccine = (
            Vaccine.query.options(joinedload("laboratories")).filter(*filters).one()
        )
    except MultipleResultsFound:
        raise DefaultException("vaccine_already_exists", code=409)
    except NoResultFound:
        raise DefaultException("vaccine_not_found", code=404)
    if vaccine.id != vaccine_id:
        raise DefaultException("vaccine_not_found", code=404)

    new_laboratory_ids = set(data.get("laboratory_ids"))
    vaccine_laboratory_ids = {laboratory.id for laboratory in vaccine.laboratories}

    if vaccine_laboratory_ids != new_laboratory_ids:
        new_laboratories = _get_laboratories_and(laboratory_ids=new_laboratory_ids)
        vaccine.laboratories = new_laboratories

    vaccine.name = name
    vaccine.pni_code = data.get("pni_code")
    vaccine.belongs_to_vaccine_card = data.get("belongs_to_vaccine_card")
    vaccine.current = data.get("current")
    vaccine.export_to_esus = data.get("export_to_esus")
    vaccine.controls_vaccine_batch = data.get("controls_vaccine_batch")
    vaccine.oblige_establishment = data.get("oblige_establishment")

    db.session.commit()


def get_vaccine_by_name(vaccine_name: str) -> list[tuple[str, any]]:
    if len(vaccine_name) < 3:
        raise ValidationException(
            errors={"vaccine_name": "Name must be at least 3 characters long"},
            message="vaccine_short_name",
        )

    return (
        Vaccine.query.with_entities(Vaccine.id, Vaccine.name)
        .filter(Vaccine.name.ilike(f"%{vaccine_name}%"))
        .all()
    )


def get_vaccine_by_id(vaccine_id: int) -> Vaccine:
    return get_vaccine(vaccine_id=vaccine_id, options=[joinedload("laboratories")])


def get_vaccine(vaccine_id: int, options: list = None) -> Vaccine:
    query = Vaccine.query

    if options is not None:
        query = query.options(*options)

    vaccine = query.get(vaccine_id)

    if vaccine is None:
        raise DefaultException("vaccine_not_found", code=404)

    return vaccine


def _get_laboratories_and(
    laboratory_ids: list[int],
) -> list[VaccineLaboratory]:
    laboratories = VaccineLaboratory.query.filter(
        VaccineLaboratory.id.in_(laboratory_ids)
    ).all()

    laboratory_ids_db = {laboratory.id for laboratory in laboratories}

    if laboratory_ids != laboratory_ids_db:
        raise DefaultException("vaccine_laboratory_not_found", code=404)
    return laboratories
