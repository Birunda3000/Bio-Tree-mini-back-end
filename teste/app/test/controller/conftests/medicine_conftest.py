import pytest


@pytest.fixture()
def base_medicine():
    """Base medicine data"""

    medicine = {
        "name": "Amoxicilina",
    }

    return medicine
