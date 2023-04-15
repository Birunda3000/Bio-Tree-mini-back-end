import pytest


@pytest.fixture()
def base_risk_classification():
    """Base risk controller created"""

    risk_classification = {
        "patient_id": 8,
        "professional_id": 1,
        "weight": 69.48,
        "height": 1.83,
        "sys_blood_pressure": 140,
        "dia_blood_pressure": 20,
        "temperature": 35.8,
        "heart_pulse": 90,
        "respiratory_frequence": 12,
        "diabetic": False,
        "capillary_blood_glucose": 77,
        "eye_opening": "À Dor",
        "verbal_response": "Palavras incompreensíveis",
        "motor_response": "Flexão Anormal",
        "pupillary_reactivity": "Reação bilateral ao estímulo",
        "fasting": False,
        "professional_avaliation": "Professional Avaliation",
        "risk_classification": "Urgente",
    }

    return risk_classification
