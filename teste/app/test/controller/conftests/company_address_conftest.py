import pytest


@pytest.fixture()
def base_company_address():
    """Base company address data"""

    company_address = {
        "street": "Rua São Damião",
        "district": "Presidente Kennedy",
        "city": "Fortaleza",
        "state": "CE",
        "complement": "Proximo a farmacia",
        "number": "871",
        "cep": "60355265",
        "municipality": "Fortaleza",
        "latitude": 3.727380,
        "longitude": 38.570772,
        "sanitary_district_id": 1,
        "regional_health": "Regional III ",
        "microregion": "Metropolitana de Fortaleza",
        "assistance_module": "Módulo de assistência",
    }

    return company_address
