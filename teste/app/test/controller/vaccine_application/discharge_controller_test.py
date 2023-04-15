import pytest

from app.main import db
from app.main.service import (
    change_patient_queue,
    create_default_queues,
    datetime_from_string,
    get_vaccine_application,
)
from app.test.seeders import (
    create_base_seed_patient,
    create_base_seed_professional,
    create_base_seed_queue_manager,
    create_base_seed_risk_classification,
    create_base_seed_vaccine_application,
)


@pytest.fixture(scope="module")
def seeded_database(database):
    """Seed database with vaccines applications"""
    create_default_queues()
    create_base_seed_professional(db)
    create_base_seed_patient(db)
    create_base_seed_queue_manager(db)
    create_base_seed_vaccine_application(db)
    create_base_seed_risk_classification(db)


@pytest.mark.usefixtures("seeded_database")
class TestVaccineApplicationDischargeController:

    # --------------------- CREATE VACCINE APPLICATION ---------------------

    @pytest.mark.parametrize(
        "key_popped",
        [
            "professional_id",
            "patient_id",
            "vaccine_name",
            "pregnancy_type",
            "complement",
        ],
        ids=[
            "without_professional_id",
            "without_patient_id",
            "without_vaccine_name",
            "without_pregnancy_type",
            "without_complement",
        ],
    )
    def test_create_vaccine_application_without_required_data(
        self, client, base_vaccine_application_discharge, key_popped
    ):
        base_vaccine_application_discharge.pop(key_popped, None)

        response = client.post(
            "/vaccine_application/discharge",
            json=base_vaccine_application_discharge,
        )

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert key_popped in response.json["errors"].keys()

    @pytest.mark.parametrize(
        "key,new_value,expected_message",
        [
            ("patient_id", 0, "patient_not_found"),
            ("professional_id", 0, "professional_not_found"),
        ],
        ids=[
            "invalid_patient_id",
            "invalid_professional_id",
        ],
    )
    def test_create_vaccine_application_with_invalid_data(
        self,
        client,
        base_vaccine_application_discharge,
        key,
        new_value,
        expected_message,
    ):
        base_vaccine_application_discharge[key] = new_value

        response = client.post(
            "/vaccine_application/discharge",
            json=base_vaccine_application_discharge,
        )

        assert response.status_code == 404
        assert response.json["message"] == expected_message

    @pytest.mark.parametrize(
        "key,new_value",
        [
            ("administration_route", "invalid_administration_route"),
            ("application_site", "invalid_application_site"),
            ("pregnancy_type", "invalid_pregnancy_type"),
            ("complement", "invalid_complement"),
        ],
        ids=[
            "invalid_administration_route",
            "invalid_application_site",
            "invalid_pregnancy_type",
            "invalid_complement",
        ],
    )
    def test_create_vaccine_application_with_invalid_dto_data(
        self, client, base_vaccine_application_discharge, key, new_value
    ):
        base_vaccine_application_discharge[key] = new_value

        response = client.post(
            "/vaccine_application/discharge",
            json=base_vaccine_application_discharge,
        )

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert key in response.json["errors"].keys()

    def test_create_vaccine_application_with_patient_not_in_vaccination_queue(
        self, client, base_vaccine_application_discharge
    ):

        response = client.post(
            "/vaccine_application/discharge",
            json=base_vaccine_application_discharge,
        )

        assert response.status_code == 409
        assert response.json["message"] == "patient_not_in_vaccination_queue"

    def test_create_vaccine_application(
        self, client, base_vaccine_application_discharge
    ):
        change_patient_queue({"patient_id": 1, "queue_id": 5})

        response = client.post(
            "/vaccine_application/discharge",
            json=base_vaccine_application_discharge,
        )

        assert response.status_code == 201
        assert response.json["message"] == "vaccine_application_created"

        change_patient_queue({"patient_id": 1, "queue_id": 1})
