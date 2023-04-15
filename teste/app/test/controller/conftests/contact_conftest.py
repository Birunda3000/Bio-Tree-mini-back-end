import pytest


@pytest.fixture()
def base_contact():
    """Base contact data"""

    contact = {
        "phone": "8532165498",
        "cellphone": "85987654321",
        "emergency_contact": "85987654321",
        "fax": "fax",
    }

    return contact
