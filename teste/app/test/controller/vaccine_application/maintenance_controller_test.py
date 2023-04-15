from datetime import date, timedelta

import pytest

from app.main import db
from app.main.service import date_to_string, get_vaccine_application
from app.test.seeders import (
    create_base_seed_patient,
    create_base_seed_professional,
    create_base_seed_queue_manager,
    create_base_seed_risk_classification,
    create_base_seed_vaccine,
    create_base_seed_vaccine_application,
    create_base_seed_vaccine_laboratory,
)


@pytest.fixture(scope="module")
def seeded_database(database):
    """Seed database with vaccines applications"""
    create_base_seed_patient(db)
    create_base_seed_professional(db)
    create_base_seed_queue_manager(db)
    create_base_seed_risk_classification(db)
    create_base_seed_vaccine_laboratory(db)
    create_base_seed_vaccine(db)
    create_base_seed_vaccine_application(db)


@pytest.mark.usefixtures("seeded_database")
class TestVaccineApplicationMaintenanceController:

    # --------------------- POST ---------------------

    @pytest.mark.parametrize(
        "key_popped",
        [
            "vaccine_application_id",
            "performed_at",
        ],
        ids=[
            "without_vaccine_application_id",
            "without_performed_at",
        ],
    )
    def test_create_vaccine_application_maintenance_without_required_data(
        self, client, base_vaccine_application_maintenance, key_popped
    ):
        base_vaccine_application_maintenance.pop(key_popped, None)

        response = client.post(
            "/vaccine_application_maintenance",
            json=base_vaccine_application_maintenance,
        )

        assert response.json["message"] == "Input payload validation failed"
        assert key_popped in response.json["errors"].keys()
        assert response.status_code == 400

    @pytest.mark.parametrize(
        "key,new_value,expected_message",
        [
            ("vaccine_application_id", 0, "vaccine_application_not_found"),
        ],
        ids=[
            "invalid_vaccine_application_id",
        ],
    )
    def test_create_vaccine_application_maintenance_with_invalid_data(
        self,
        client,
        base_vaccine_application_maintenance,
        key,
        new_value,
        expected_message,
    ):
        base_vaccine_application_maintenance[key] = new_value

        response = client.post(
            "/vaccine_application_maintenance",
            json=base_vaccine_application_maintenance,
        )

        assert response.json["message"] == expected_message
        assert response.status_code == 404

    @pytest.mark.parametrize(
        "key,new_value",
        [
            (
                "performed_at",
                date_to_string(date.today() + timedelta(days=1)),
            )
        ],
        ids=[
            "invalid_performed_at",
        ],
    )
    def test_create_vaccine_application_maintenance_with_invalid_dto_data(
        self, client, base_vaccine_application_maintenance, key, new_value
    ):
        base_vaccine_application_maintenance[key] = new_value

        response = client.post(
            "/vaccine_application/application",
            json=base_vaccine_application_maintenance,
        )

        assert response.json["message"] == "Input payload validation failed"
        assert key in response.json["errors"].keys()
        assert response.status_code == 400

    def test_create_vaccine_application_maintenance_with_not_accepted_application_type(
        self, client, base_vaccine_application_maintenance
    ):
        base_vaccine_application_maintenance["vaccine_application_id"] = 2

        response = client.post(
            "/vaccine_application_maintenance",
            json=base_vaccine_application_maintenance,
        )

        assert (
            response.json["message"]
            == "vaccine_application_maintenance_not_accepted_application_type"
        )
        assert response.status_code == 409

    @pytest.mark.parametrize(
        "vaccine_application_id",
        [3, 5],
        ids=["edited_vaccine_application", "deleted_vaccine_application"],
    )
    def test_create_vaccine_application_maintenance_with_invalid_vaccine_application(
        self, client, base_vaccine_application_maintenance, vaccine_application_id
    ):

        self._able_vaccine_to_be_edited_and_deleted(
            vaccine_application_id=vaccine_application_id
        )

        base_vaccine_application_maintenance[
            "vaccine_application_id"
        ] = vaccine_application_id

        response = client.post(
            "/vaccine_application_maintenance",
            json=base_vaccine_application_maintenance,
        )

        assert (
            response.json["message"]
            == "vaccine_application_maintenance_invalid_vaccine_application"
        )
        assert response.status_code == 409

    def test_create_vaccine_application_maintenance_with_vaccine_application_time_exceeded(
        self, client, base_vaccine_application_maintenance
    ):

        base_vaccine_application_maintenance["vaccine_application_id"] = 1

        response = client.post(
            "/vaccine_application_maintenance",
            json=base_vaccine_application_maintenance,
        )

        assert (
            response.json["message"]
            == "vaccine_application_maintenance_vaccine_application_time_exceeded"
        )
        assert response.status_code == 409

    def test_create_vaccine_application_maintenance(
        self, client, base_vaccine_application_maintenance
    ):

        self._able_vaccine_to_be_edited_and_deleted(
            vaccine_application_id=base_vaccine_application_maintenance.get(
                "vaccine_application_id"
            )
        )

        response = client.post(
            "/vaccine_application_maintenance",
            json=base_vaccine_application_maintenance,
        )

        assert response.json["message"] == "vaccine_application_maintenance_created"
        assert response.status_code == 201

    # --------------------- DELETE ---------------------

    def test_delete_vaccine_application_maintenance_with_non_registered_vaccine_application_id(
        self, client
    ):
        response = client.delete(
            "/vaccine_application_maintenance/0", json={"reason": "delete reason"}
        )

        assert response.json["message"] == "vaccine_application_not_found"
        assert response.status_code == 404

    def test_delete_vaccine_application_maintenance_with_not_accepted_application_type(
        self, client
    ):
        response = client.delete(
            "/vaccine_application_maintenance/2", json={"reason": "delete reason"}
        )

        assert (
            response.json["message"]
            == "vaccine_application_maintenance_not_accepted_application_type"
        )
        assert response.status_code == 409

    @pytest.mark.parametrize(
        "vaccine_application_id",
        [3, 5],
        ids=["edited_vaccine_application", "deleted_vaccine_application"],
    )
    def test_delete_vaccine_application_maintenance_with_invalid_vaccine_application(
        self, client, vaccine_application_id
    ):
        response = client.delete(
            f"/vaccine_application_maintenance/{vaccine_application_id}",
            json={"reason": "delete reason"},
        )

        assert (
            response.json["message"]
            == "vaccine_application_maintenance_invalid_vaccine_application"
        )
        assert response.status_code == 409

    def test_delete_vaccine_application_maintenance_with_vaccine_application_time_exceeded(
        self, client
    ):
        response = client.delete(
            "/vaccine_application_maintenance/4", json={"reason": "delete reason"}
        )

        assert (
            response.json["message"]
            == "vaccine_application_maintenance_vaccine_application_time_exceeded"
        )
        assert response.status_code == 409

    def test_delete_vaccine_application_maintenance(self, client):

        self._able_vaccine_to_be_edited_and_deleted(vaccine_application_id=4)

        response = client.delete(
            "/vaccine_application_maintenance/4", json={"reason": "delete reason"}
        )

        assert response.json["message"] == "vaccine_application_maintenance_deleted"
        assert response.status_code == 200

    # --------------------- Helper Functions ---------------------

    def _able_vaccine_to_be_edited_and_deleted(
        self, vaccine_application_id: int
    ) -> None:
        vaccine_application = get_vaccine_application(
            vaccine_application_id=vaccine_application_id
        )

        vaccine_application.performed_at = date.today()

        db.session.commit()
