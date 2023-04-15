import pytest


@pytest.fixture()
def base_vaccine_application_application():
    """Base data"""
    vaccine_application = {
        "professional_id": 1,
        "patient_id": 1,
        "request_id": 1,
        "vaccine_name": "BCG",
        "manufacturer": "F.A.P. - FUNDACAO ATAULPHO DE PAIVA",
        "batch": "1x78147",
        "administration_route": "Oral",
        "application_site": "Boca",
        "bottle_type": "Frasco",
        "bottle_doses_number": 1,
        "pregnancy_type": "Gestante",
        "performed_at": "17/11/2021",
    }

    return vaccine_application


@pytest.fixture()
def base_vaccine_application_discharge():
    """Base data"""
    vaccine_application = {
        "professional_id": 1,
        "patient_id": 1,
        "vaccine_name": "Hepatite B",
        "manufacturer": "F.A.P. - FUNDACAO ATAULPHO DE PAIVA",
        "batch": "1x78147",
        "pregnancy_type": "Gestante",
        "complement": "Documento",
        "performed_at": "17/11/2021",
    }

    return vaccine_application
