import pytest


@pytest.fixture()
def base_patient(base_address, base_contact):
    """Base patient data"""

    patient = {
        "name": "Novo patient teste",
        "social_name": "Patient social name",
        "cpf": "34326261005",
        "email": "patient999@test.com",
        "birth": "10/10/1996",
        "sex": "Feminino",
        "mother_name": "Mãe novo patient",
        "father_name": "Pai novo patient",
        "cns_cod": "921539636200004",
        "gender": "HOMEM CIS",
        "medical_number": 1,
        "breed": "BRANCO",
        "address": base_address,
        "contact": base_contact,
    }

    return patient
