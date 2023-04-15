import pytest


@pytest.fixture()
def base_medical_appointment():
    """Base medical appointment data"""

    medical_appointment = {
        "patient_id": 1,
        "professional_id": 1,
        "description": "Febrio",
        "diagnosis_type": "Definitivo",
        "diagnosis_work": "Sim",
        "diagnosis_traffic_accident": "Não",
    }

    return medical_appointment
