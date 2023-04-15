import pytest


@pytest.fixture()
def base_institution_type():
    """Base institution type base"""
    institution_type = {
        "name": "institution type 1",
    }

    return institution_type


@pytest.fixture()
def base_institution_subtype():
    """Base institution subtype base"""
    institution_subtype = {
        "institution_type_id": 1,
        "name": "institution subtype 1",
    }

    return institution_subtype
