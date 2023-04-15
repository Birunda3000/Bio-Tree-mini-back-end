import pytest


@pytest.fixture()
def base_death_launch():
    death_launch = {
        "patient_id": 3,
        "cid_10_id": 2,
        "professional_id": 1,
        "certificate_number": 3,
        "place": "Sala X",
        "circunstances_of_death": "circunstancia teste 3",
        "datetime_of_death": "03/11/2022 22:30:00",
        "registration_datetime": "03/11/2022 23:30:30",
    }

    return death_launch


@pytest.fixture()
def base_death_launch_update():
    base_death_launch_update = {
        "cid_10_id": 2,
        "professional_id": 1,
        "certificate_number": 3,
        "place": "Sala X",
        "circunstances_of_death": "circunstancia teste 3",
        "datetime_of_death": "03/11/2022 22:30:00",
        "registration_datetime": "03/11/2022 23:30:30",
    }

    return base_death_launch_update
