import pytest


@pytest.fixture()
def base_equipment():
    """Base equipment"""

    equipment = {"name": "equipamento teste", "equipment_type_id": 1}

    return equipment


@pytest.fixture()
def base_equipment_type():
    """Base equipment type"""

    equipment_type = {"name": "tipo de equipamento teste"}

    return equipment_type
