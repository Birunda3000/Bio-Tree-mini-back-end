import pytest


@pytest.fixture()
def base_diagnosis():
    """Base diagnosis data"""
    diagnosis = {"protocol_id": 5, "questions_ids": [2]}

    return diagnosis
