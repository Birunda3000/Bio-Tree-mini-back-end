import pytest


@pytest.fixture()
def base_admission():
    """Base admission data"""
    admission = {
        "patient_id": 9,
        "professional_id": 1,
        "bed_id": 1,
        "type": "Observação",
    }

    return admission
