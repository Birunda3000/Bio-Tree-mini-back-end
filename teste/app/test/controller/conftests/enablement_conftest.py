import pytest


@pytest.fixture()
def base_enablement():
    """Base enablement data"""
    enablement = {
        "code": "0003",
        "name": "Habilitação teste 3",
        "number_of_beds": 100,
        "ordinance_number": 3,
        "release_date": "01/01/1990",
    }

    return enablement
