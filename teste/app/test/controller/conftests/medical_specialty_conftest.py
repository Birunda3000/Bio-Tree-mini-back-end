import pytest


@pytest.fixture()
def base_medical_specialty():
    """Base medical specialty"""

    medical_specialty = {"name": "teste"}

    return medical_specialty
