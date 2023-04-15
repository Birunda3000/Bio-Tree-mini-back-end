import pytest


@pytest.fixture()
def base_medical_prescription_orientation():
    """Base medical prescription orientation data"""

    orientation = {
        "orientation": "Orientation One",
        "execute_at": "03/11/2022 21:30:30",
        "observations": "Orientation Observation",
    }

    return orientation


@pytest.fixture()
def base_medical_prescription_medicine():
    """Base medical prescription orientation data"""

    medicine = {
        "medicine_id": 1,
        "execute_at": "03/11/2022 21:30:30",
        "observations": "Medicine Observation",
    }

    return medicine


@pytest.fixture()
def base_medical_prescription_procedure():
    """Base medical prescription orientation data"""

    procedure = {
        "procedure_id": 1,
        "execute_at": "03/11/2022 21:30:30",
        "observations": "Procedure Observation",
    }

    return procedure


@pytest.fixture()
def base_medical_prescription(
    base_medical_prescription_orientation,
    base_medical_prescription_medicine,
    base_medical_prescription_procedure,
):
    """Base medical prescription data"""

    medical_appointment = {
        "professional_id": 1,
        "patient_id": 1,
        "room_id": 1,
        "type": "Observação",
        "orientations": [base_medical_prescription_orientation],
        "medicines": [base_medical_prescription_medicine],
        "procedures": [base_medical_prescription_procedure],
    }

    return medical_appointment
