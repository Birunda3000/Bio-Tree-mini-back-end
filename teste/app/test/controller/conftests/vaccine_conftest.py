import pytest


@pytest.fixture()
def base_vaccine():
    """Base vaccine data"""
    vaccine = {
        "name": "Vacina teste",
        "pni_code": "00123",
        "belongs_to_vaccine_card": True,
        "current": True,
        "export_to_esus": False,
        "controls_vaccine_batch": True,
        "oblige_establishment": False,
        "laboratory_ids": [1],
    }

    return vaccine


@pytest.fixture()
def base_vaccine_laboratory():
    """Base vaccine laboratory data"""
    vaccine_laboratory = {
        "name": "Laboratorio teste",
        "pni_code": "COD000",
        "cnpj": "60972319000100",
    }

    return vaccine_laboratory
