import pytest


@pytest.fixture()
def base_professional_bond():
    """Base professional_bond data"""

    base_professional_bond = {
        "preceptor_professional_id": 1,
        "professional_id": 1,
        "occupation_id": 20,
        "contract_type": "contrato de trabalho",
        "contract_number": "123456789",
        "edict_number": "123456789",
        "type_of_bond": "CLT",
        "contract_start": "10/10/2014",
        "contract_end": "10/10/2014",
        "workload_ambulance": "10/10/2014 04:26:14",
        "workload_hospital": "10/10/2014 04:26:14",
        "workload_others": "10/10/2014 04:26:14",
        "attends_sus": True,
        "attends_apac": False,
        "employer_cnpj": "123456789",
        "legal_nature": "123456789",
    }
