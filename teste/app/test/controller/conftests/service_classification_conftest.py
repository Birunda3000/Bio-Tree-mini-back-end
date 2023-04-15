import pytest


@pytest.fixture()
def base_service():
    """Base service base"""
    service = {
        "code": "003",
        "name": "SERVICE THREE",
    }

    return service


@pytest.fixture()
def base_classification():
    """Base classification base"""
    classification = {
        "service_id": 1,
        "code": "003",
        "name": "CLASSIFICATION THREE",
    }

    return classification
