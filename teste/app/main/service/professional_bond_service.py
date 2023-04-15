from app.main import db
from app.main.config import Config
from app.main.enum import *
from app.main.exceptions import DefaultException
from app.main.model import Agency, Occupation, ProfessionalBond
from app.main.service import date_from_string, datetime_from_string
from app.main.service.fces import get_fces
from app.main.service.professional_service import get_professional

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def get_professional_bonds(professional_id: int) -> list[ProfessionalBond]:
    professional = get_professional(professional_id=professional_id)
    return {
        "items": professional.professional_bonds,
    }


def add_professional_bond(professional_id: int, data: dict[str, any]) -> None:
    fces = get_fces(fces_id=data.get("fces_id"))
    occupation = check_if_professional_has_occupation(
        professional_id=professional_id, occupation_id=data.get("occupation_id")
    )
    professional = get_professional(professional_id=professional_id)
    preceptor = get_professional(professional_id=data.get("preceptor_professional_id"))

    new_professional_bond = ProfessionalBond(
        contract_type=data.get("contract_type"),
        contract_number=data.get("contract_number"),
        edict_number=data.get("edict_number"),
        type_of_bond=data.get("type_of_bond"),
        contract_start=date_from_string(value=data.get("contract_start")),
        contract_end=date_from_string(value=data.get("contract_end")),
        workload_ambulance=datetime_from_string(value=data.get("workload_ambulance")),
        workload_hospital=datetime_from_string(value=data.get("workload_hospital")),
        workload_others=datetime_from_string(value=data.get("workload_others")),
        attends_sus=data.get("attends_sus"),
        attends_apac=data.get("attends_apac"),
        employer_cnpj=data.get("employer_cnpj"),
        legal_nature=data.get("legal_nature"),
        professional=professional,
        preceptor_professional=preceptor,
        occupation=occupation,
        fces=fces,
    )
    db.session.add(new_professional_bond)
    db.session.commit()


def update_professional_bond(professional_bond_id: int, data: dict[str, any]) -> None:
    professional_bond = get_professional_bond(professional_bond_id=professional_bond_id)

    professional_bond.professional = get_professional(
        professional_id=data.get("professional_id")
    )

    professional_bond.professional.fces = get_fces(fces_id=data.get("fces_id"))

    professional_bond.professional = get_professional(
        professional_id=data.get("professional_id")
    )

    occupation = check_if_professional_has_occupation(
        professional_id=professional_bond.professional.id,
        occupation_id=data.get("occupation_id"),
    )

    preceptor = get_professional(professional_id=data.get("preceptor_professional_id"))

    professional_bond.preceptor_professional = preceptor
    professional_bond.occupation = occupation
    professional_bond.contract_type = data.get("contract_type")
    professional_bond.contract_number = data.get("contract_number")
    professional_bond.edict_number = data.get("edict_number")
    professional_bond.type_of_bond = data.get("type_of_bond")
    professional_bond.contract_start = date_from_string(
        value=data.get("contract_start")
    )
    professional_bond.contract_end = date_from_string(value=data.get("contract_end"))
    professional_bond.workload_ambulance = datetime_from_string(
        value=data.get("workload_ambulance")
    )
    professional_bond.workload_hospital = datetime_from_string(
        value=data.get("workload_hospital")
    )
    professional_bond.workload_others = datetime_from_string(
        value=data.get("workload_others")
    )
    professional_bond.attends_sus = data.get("attends_sus")
    professional_bond.attends_apac = data.get("attends_apac")
    professional_bond.employer_cnpj = data.get("employer_cnpj")
    professional_bond.legal_nature = data.get("legal_nature")
    db.session.commit()


def get_professional_bond(professional_bond_id: int) -> ProfessionalBond:
    professional_bond = ProfessionalBond.query.get(professional_bond_id)
    if professional_bond is None:
        raise DefaultException("professional_bond_not_found", code=404)
    return professional_bond


def delete_professional_bond(professional_bond_id: int) -> None:
    professional_bond = get_professional_bond(professional_bond_id=professional_bond_id)
    db.session.delete(professional_bond)
    db.session.commit()


def create_default_agencies_and_occupations(
    PATH: str = "./seeders/resources/occupations.txt",
) -> None:
    """Create the default agencies and occupations"""
    with open(PATH, "r", encoding="utf-8") as FILE:
        dicionary = treat_occupation_file(FILE)
        for key, value in dicionary.items():
            new_agency = Agency(
                name=key,
            )
            db.session.add(new_agency)
            for item in value:
                new_occuption = Occupation(
                    name=item,
                    agency=new_agency,
                )
                db.session.add(new_occuption)
    db.session.commit()


def treat_occupation_file(FILE) -> dict:
    """Treat the occupation file to create the agencies and occupations"""
    dicionary = {}
    aux = []
    for line in FILE:
        if line.startswith("["):
            pass
        elif line.startswith("]"):
            dicionary[key] = aux
            aux = []
        elif line.startswith('"'):
            trated = line.replace('"', "")
            trated = trated.replace("\n", "")
            trated = trated.replace(",", "")
            trated = trated.strip()
            aux.append(trated)
        else:
            key = line.strip()
    return dicionary


def check_if_professional_has_occupation(
    professional_id: int, occupation_id: int
) -> Occupation:
    """Check if a professional has a regional council with this occupation if has, return the occupation if not raise an exception"""
    professional = get_professional(professional_id=professional_id)
    for regional_council in professional.regional_councils:
        for occupation in regional_council.agency.occupations:
            if occupation.id == occupation_id:
                return occupation
    raise DefaultException(
        "professional_does_not_have_a_regional_council_with_this_occupation", code=400
    )
