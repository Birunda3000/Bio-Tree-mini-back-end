import pytest


@pytest.fixture()
def base_history_medical_prescription_medicine():
    """Base history medical prescription medicine data"""
    history_medical_prescription_medicine = {
        "id": 1,
        "operation_type": "Realização",
        "performed_at": "17/11/2022 22:15:00",
    }

    return history_medical_prescription_medicine


@pytest.fixture()
def base_history_medical_prescription_orientation():
    """Base history medical prescription orientation data"""
    history_medical_prescription_orientation = {
        "id": 1,
        "operation_type": "Realização",
        "performed_at": "17/11/2022 22:15:00",
    }

    return history_medical_prescription_orientation


@pytest.fixture()
def base_history_medical_prescription_procedure():
    """Base history medical prescription procedure data"""
    history_medical_prescription_procedure = {
        "id": 1,
        "operation_type": "Realização",
        "performed_at": "17/11/2022 22:15:00",
    }

    return history_medical_prescription_procedure


@pytest.fixture()
def base_clinical_evolution_history(
    base_history_medical_prescription_medicine,
    base_history_medical_prescription_orientation,
    base_history_medical_prescription_procedure,
):
    """Base clinical evolution history"""
    clinical_evolution_history = {
        "admission_id": 1,
        "professional_id": 1,
        "medical_prescription_medicines_data": [
            base_history_medical_prescription_medicine
        ],
        "medical_prescription_orientations_data": [
            base_history_medical_prescription_orientation
        ],
        "medical_prescription_procedures_data": [
            base_history_medical_prescription_procedure
        ],
    }

    return clinical_evolution_history
