import pytest


@pytest.fixture()
def base_prescription():
    """Base prescription data"""

    prescription = {"protocol_id": 3, "actions_ids": [1]}

    return prescription
