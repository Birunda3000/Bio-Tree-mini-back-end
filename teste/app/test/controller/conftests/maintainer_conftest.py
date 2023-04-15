import pytest


@pytest.fixture()
def base_maintainer(base_address, base_contact):
    """Base maintainer data"""

    maintainer = {
        "corporate_name": "Novo maintainer teste",
        "commercial_name": "Maintainer commercial name ",
        "cnpj": "19067705000154",
        "regional_number": 1,
        "unit_type": "Privada lucrativa simples",
        "email": "maintainer999@test.com",
        "address": base_address,
        "contact": base_contact,
    }

    return maintainer
