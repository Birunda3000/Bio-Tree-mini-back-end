import pytest


@pytest.fixture()
def base_vital_signs_control():
    """Base vital signs control data"""
    vital_signs_control = {
        "sys_blood_pressure": 110,
        "dia_blood_pressure": 90,
        "heart_pulse": 77,
        "respiratory_frequence": 13,
        "body_fat_rate": 18,
        "temperature": 37.0,
        "oxygen_saturation": 96,
    }

    return vital_signs_control
