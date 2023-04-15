import pytest


@pytest.fixture()
def base_vaccine_application_request():
    """Base data"""
    vaccine_application_request = {
        "professional_id": 1,
        "patient_id": 1,
        "vaccine_id": 1,
    }

    return vaccine_application_request
