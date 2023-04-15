import pytest


@pytest.fixture()
def base_fces(base_company_address, base_contact):
    """Base fces data"""

    fces = {
        "maintainer_id": 1,
        "professional_id": 1,
        "corporate_name": "Estabelecimento Teste 4",
        "commercial_name": "Estabelecimento teste 4",
        "cnes_code": 55568651,
        "person_type": "Jurídica",
        "cnpj": "48248576000107",
        "email": "string4@example.br",
        "establishment_code": 265591,
        "situation": "Individual",
        "establishment_type": "Tipo de estabelecimento",
        "establishment_subtype": "Subtipo de estabelecimento",
        "regulatory_registration_end_date": "Data de término do registro regulamentar",
        "payment_to_provider": "Fixo",
        "company_address": base_company_address,
        "contact": base_contact,
    }

    return fces
