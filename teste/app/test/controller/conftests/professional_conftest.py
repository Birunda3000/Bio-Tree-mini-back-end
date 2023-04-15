import pytest


@pytest.fixture()
def base_professional(base_address):
    """Base professional data"""

    professional = {
        "name": "Novo profissional teste",
        "social_name": "Novo profissional nome social",
        "email": "novo_profissional@uece.com",
        "cpf": "34326261005",
        "birth": "10/10/1996",
        "sex": "Feminino",
        "mother_name": "Mãe novo profissional",
        "father_name": "Pai novo profissional",
        "cns_cod": "921539636200004",
        "address": base_address,
    }

    dismisal_cause = {
        "dismissal_cause": "TRANSF. PARA OUTRO ESTABELECIMENTO DO MESMO MUNICÍPIO"
    }

    return professional


@pytest.fixture()
def base_professional_dismissal():
    """Dismissal professional data"""

    dismisal_cause = {
        "dismissal_cause": "TRANSF. PARA OUTRO ESTABELECIMENTO DO MESMO MUNICÍPIO"
    }

    return dismisal_cause
