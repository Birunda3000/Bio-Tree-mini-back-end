from math import ceil

from werkzeug.datastructures import ImmutableMultiDict

from app.main import db
from app.main.config import Config
from app.main.exceptions import DefaultException
from app.main.model import RegionalCouncil, Agency
from app.main.service import date_from_string, datetime_from_string, time_from_string

from ..enum import *
from .professional_service import get_professional


_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def get_regional_councils(professional_id: int) -> list[RegionalCouncil]:
    professional = get_professional(professional_id=professional_id)
    if professional is None:
        raise DefaultException("professional_not_found", code=404)
    return {
        "items": professional.regional_councils,
    }


def add_regional_council(professional_id: int, data: dict[str, any]) -> None:
    professional = get_professional(professional_id=professional_id)
    if professional is None:
        raise DefaultException("professional_not_found", code=404)
    agency = Agency.query.get(data.get("agency_id"))
    if agency is None:
        raise DefaultException("agency_not_found", code=404)
    new_regional_council = RegionalCouncil(
        professional=professional,
        agency=agency,
        regional_council_number=data.get("regional_council_number"),
        FU_of_council=data.get("FU_of_council"),
        actual=data.get("actual"),
        last_occurrence_of_SCNES=date_from_string(
            value=data.get("last_occurrence_of_SCNES")
        ),
    )
    db.session.add(new_regional_council)
    db.session.commit()


def get_regional_council(regional_council_id: int) -> RegionalCouncil:
    regional_council = RegionalCouncil.query.get(regional_council_id)
    if regional_council is None:
        raise DefaultException("regional_council_not_found", code=404)
    return regional_council


def update_regional_council(regional_council_id: int, data: dict[str, any]) -> None:
    regional_council = get_regional_council(regional_council_id=regional_council_id)
    agency = Agency.query.get(data.get("agency_id"))
    regional_council.agency = agency
    regional_council.regional_council_number = data.get("regional_council_number")
    regional_council.FU_of_council = data.get("FU_of_council")
    regional_council.actual = data.get("actual")
    regional_council.last_occurrence_of_SCNES = date_from_string(
        value=data.get("last_occurrence_of_SCNES")
    )
    db.session.commit()


def delete_regional_council(regional_council_id: int) -> None:
    regional_council = get_regional_council(regional_council_id=regional_council_id)
    check_occupation_bond(regional_council=regional_council)
    db.session.delete(regional_council)
    db.session.commit()


def check_occupation_bond(regional_council: RegionalCouncil) -> RegionalCouncil:
    '''Check if the professional has a professional_bond with an occupation belonging to this regional council'''
    professional = regional_council.professional
    for professional_bond in professional.professional_bonds:
        if professional_bond.occupation.agency == regional_council.agency:
            raise DefaultException("professional_bond_with_occupation_belonging_to_this_regional_council", code=400)
    return regional_council