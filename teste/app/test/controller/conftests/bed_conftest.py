import pytest


@pytest.fixture()
def base_bed():
    """Base bed data"""

    bed = {"bed_number": 1, "available": True, "status": True, "room_id": 1}

    return bed


@pytest.fixture()
def base_bed_type():
    """Base bed type data"""
    bed_type = {
        "name": "Tipo de cama teste 3",
    }

    return bed_type
