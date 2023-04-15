from app.main.model.professional_bond_model import ProfessionalBond
from app.main.model.professional_model import Professional
from app.main.service import (
    date_from_string,
    datetime_from_string,
    get_fces,
    get_professional,
)


def create_base_seed_professional_bond(db):
    """Add ProfessionalBonds"""
    professional = get_professional(professional_id=1)
    fces = get_fces(fces_id=1)
    new_professional_bond = ProfessionalBond(
        contract_type="from fces",
        contract_number="123456",
        edict_number="123456",
        type_of_bond="CLT",
        contract_start=date_from_string(value="24/08/1989"),
        contract_end=date_from_string(value="24/08/1989"),
        workload_ambulance=datetime_from_string(value="24/08/1989"),
        workload_hospital=datetime_from_string(value="24/08/1989"),
        workload_others=datetime_from_string(value="24/08/1989"),
        attends_sus=True,
        attends_apac=True,
        employer_cnpj="123456",
        legal_nature="123456",
        professional=professional,
        fces=fces,
    )
