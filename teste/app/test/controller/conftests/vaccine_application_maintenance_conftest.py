import pytest


@pytest.fixture()
def base_vaccine_application_maintenance():
    """Base data"""
    base_vaccine_application_maintenance = {
        "vaccine_application_id": 1,
        "performed_at": "14/02/2020",
    }

    return base_vaccine_application_maintenance
