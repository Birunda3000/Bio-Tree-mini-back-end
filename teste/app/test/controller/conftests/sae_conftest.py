import pytest


@pytest.fixture()
def base_sae_determinations_action():
    """Base sae determinations action"""
    action = {"id": 1, "recurrence": "1/1"}
    return action


@pytest.fixture()
def base_sae_determinations(base_sae_determinations_action):
    """Base sae determinations"""

    sae_determinations = {
        "admission_id": 1,
        "professional_id": 1,
        "actions": [base_sae_determinations_action],
        "questions": [1, 2],
    }

    return sae_determinations


@pytest.fixture()
def base_sae_perform_prescription():
    """Base sae perform prescription"""

    sae_perform_prescription = {
        "action_id": 1,
        "performed_at": "24/11/2022 00:22:33",
        "delete": False,
    }

    return sae_perform_prescription


@pytest.fixture()
def base_sae_perform(base_sae_perform_prescription, base_vital_signs_control):
    """Base sae perform"""

    base_vital_signs_control.setdefault("performed_at", "24/11/2022 00:22:33")

    sae_perform = {
        "admission_id": 1,
        "professional_id": 1,
        "vital_signs_control": base_vital_signs_control,
        "prescriptions_performed": [base_sae_perform_prescription],
    }

    return sae_perform
