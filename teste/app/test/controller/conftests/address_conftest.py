import pytest


@pytest.fixture()
def base_address():
    """Base address data"""

    address = {
        "street": "Rua teste",
        "district": "Fátima",
        "city": "Fortaleza",
        "state": "CE",
        "complement": "Prox ao supermercado",
        "number": "842",
        "cep": "60875590",
    }

    return address
