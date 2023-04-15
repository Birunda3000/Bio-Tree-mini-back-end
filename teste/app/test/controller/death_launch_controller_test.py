from datetime import datetime, timedelta

import pytest

from app.main import db
from app.main.service import datetime_to_string, get_queue_manager_by_patient_id
from app.test.seeders import (
    create_base_death_launch,
    create_base_seed_cid_10,
    create_base_seed_patient,
    create_base_seed_professional,
)


@pytest.fixture(scope="module")
def seeded_database(client, database):
    create_base_seed_professional(db)
    create_base_seed_patient(db)
    create_base_seed_cid_10(db)
    create_base_death_launch(db)


@pytest.mark.usefixtures("seeded_database")
class TestDeathLaunchController:

    # --------------------- GET ---------------------

    def test_get_death_launches(self, client):
        response = client.get("/death_launch")

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 2
        assert response.json["total_pages"] == 1
        self._test_get_death_launch_list_item(data=response.json["items"][0])

    @pytest.mark.parametrize(
        "query_string, total_items",
        [
            ({"patient_name": "Patient social name 1"}, 1),
            ({"patient_name": "1"}, 1),
            ({"responsible_for_registration": "Profissional teste 1"}, 1),
            ({"responsible_for_registration": "1"}, 1),
            ({"start_date_of_death": "25/08/1989"}, 2),
            (
                {
                    "start_date_of_death": "25/08/1989",
                    "end_date_of_death": "24/07/2004",
                },
                1,
            ),
            ({"start_registration_date": "25/08/1989"}, 2),
            (
                {
                    "start_registration_date": "25/08/1989",
                    "end_registration_date": "24/07/2004",
                },
                1,
            ),
        ],
        ids=[
            "complete_patient_name",
            "incomplete_patient_name",
            "complete_responsible_for_registration_name",
            "incomplete_responsible_for_registration_name",
            "only_start_date_of_death",
            "start_and_end_date_of_death",
            "only_start_registration_date",
            "start_and_end_registration_date",
        ],
    )
    def test_get_death_launches_by_query_parameters(
        self, client, query_string, total_items
    ):
        response = client.get("/death_launch", query_string=query_string)

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == total_items
        assert response.json["total_pages"] == 1
        self._test_get_death_launch_list_item(data=response.json["items"][0])

    # --------------------- GET BY ID ---------------------

    def test_get_death_launch_by_id(self, client):
        response = client.get("/death_launch/1")

        assert response.status_code == 200
        assert response.json["id"] == 1
        assert response.json["certificate_number"] == 1
        assert response.json["circunstances_of_death"] == "circustancia teste 1"
        assert response.json["place"] == "Sala X"
        assert response.json["datetime_of_death"] == "25/08/1989 18:00:00"
        assert response.json["registration_datetime"] == "25/08/1989 23:40:00"
        assert response.json["professional"] == {
            "id": 1,
            "name": "Profissional teste 1",
            "social_name": "Profissional teste 1 nome social",
        }
        assert response.json["cid_10"] == {"id": 1, "code": "S02", "category": 19}
        assert response.json["patient"] == {
            "id": 1,
            "name": "Patient teste 1",
            "social_name": "Patient social name 1",
            "sex": "Masculino",
            "birth": "24/08/1989",
        }

    def test_get_death_launch_by_non_registered_id(self, client):
        response = client.get("/death_launch/0")

        assert response.status_code == 404
        assert response.json["message"] == "death_launch_not_found"

    # --------------------- UPDATE ---------------------

    def test_update_death_launch_with_non_registered_id(
        self, client, base_death_launch_update
    ):
        response = client.put("/death_launch/0", json=base_death_launch_update)

        assert response.status_code == 404
        assert response.json["message"] == "death_launch_not_found"

    @pytest.mark.parametrize(
        "key,value,message",
        [
            ("cid_10_id", 0, "cid_10_not_found"),
            ("professional_id", 0, "professional_not_found"),
        ],
        ids=[
            "invalid_cid_10_id",
            "invalid_professional_id",
        ],
    )
    def test_update_death_launch_with_invalid_relationship(
        self, client, base_death_launch, key, value, message
    ):
        base_death_launch[key] = value
        response = client.put("/death_launch/1", json=base_death_launch)

        assert response.status_code == 404
        assert response.json["message"] == message

    @pytest.mark.parametrize(
        "key_popped",
        [
            "datetime_of_death",
            "registration_datetime",
            "certificate_number",
            "cid_10_id",
            "place",
            "professional_id",
        ],
        ids=[
            "update_without_datetime_of_death",
            "update_without_registration_datetime",
            "update_without_certificate_number",
            "update_without_cid_10_id",
            "update_without_place",
            "update_without_professional_id",
        ],
    )
    def test_update_death_launch_without_required_data(
        self, client, base_death_launch, key_popped
    ):
        base_death_launch.pop(key_popped)
        response = client.put("/death_launch/1", json=base_death_launch)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert key_popped in response.json["errors"].keys()

    @pytest.mark.parametrize(
        "key",
        ["datetime_of_death", "registration_datetime"],
        ids=[
            "datetime_of_death",
            "registration_datetime",
        ],
    )
    def test_update_death_launch_with_future_datetime(
        self, client, base_death_launch_update, key
    ):
        base_death_launch_update[key] = datetime_to_string(
            datetime.now() + timedelta(days=2)
        )
        response = client.put("/death_launch/1", json=base_death_launch_update)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert key in response.json["errors"].keys()

    def test_update_death_launch(self, client, base_death_launch_update):
        response = client.put("/death_launch/1", json=base_death_launch_update)

        assert response.json["message"] == "death_launch_updated"
        assert response.status_code == 200

    # --------------------- POST ---------------------

    @pytest.mark.parametrize(
        "key,value,message",
        [
            ("cid_10_id", 0, "cid_10_not_found"),
            ("patient_id", 0, "patient_not_found"),
            ("professional_id", 0, "professional_not_found"),
        ],
        ids=["invalid_cid_10_id", "invalid_patient_id", "invalid_professional_id"],
    )
    def test_create_death_launch_with_invalid_relationship(
        self, client, base_death_launch, key, value, message
    ):
        base_death_launch[key] = value
        response = client.post("/death_launch", json=base_death_launch)

        assert response.status_code == 404
        assert response.json["message"] == message

    @pytest.mark.parametrize(
        "key_popped",
        [
            "patient_id",
            "cid_10_id",
            "professional_id",
            "datetime_of_death",
            "certificate_number",
            "place",
            "registration_datetime",
        ],
        ids=[
            "without_patient_id",
            "without_cid_10_id",
            "without_professional_id",
            "without_datetime_of_death",
            "without_certificate_number",
            "without_place",
            "without_registration_datetime",
        ],
    )
    def test_create_death_launch_without_required_data(
        self, client, base_death_launch, key_popped
    ):
        base_death_launch.pop(key_popped)
        response = client.post("/death_launch", json=base_death_launch)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert key_popped in response.json["errors"].keys()

    @pytest.mark.parametrize(
        "key",
        ["datetime_of_death", "registration_datetime"],
        ids=[
            "datetime_of_death",
            "registration_datetime",
        ],
    )
    def test_create_death_launch_with_future_datetime(
        self, client, base_death_launch, key
    ):
        base_death_launch[key] = datetime_to_string(datetime.now() + timedelta(days=2))
        response = client.post("/death_launch", json=base_death_launch)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert key in response.json["errors"].keys()

    def test_create_death_launch_with_patient_already_with_launch_register(
        self, client, base_death_launch
    ):
        base_death_launch["patient_id"] = 1
        response = client.post("/death_launch", json=base_death_launch)

        assert response.status_code == 409
        assert response.json["message"] == "patient_already_has_death_launch"

    def test_create_death_launch_with_patient_in_queue(self, client, base_death_launch):
        response = client.post("/death_launch", json=base_death_launch)

        assert response.json["message"] == "death_launch_created"
        assert response.status_code == 201

        assert (
            get_queue_manager_by_patient_id(patient_id=base_death_launch["patient_id"])
            is None
        )

    def test_create_death_launch_with_patient_without_queue_manager(
        self, client, base_death_launch
    ):
        base_death_launch["patient_id"] = 10
        response = client.post("/death_launch", json=base_death_launch)

        assert response.json["message"] == "death_launch_created"
        assert response.status_code == 201

    # --------------------- DELETE ---------------------

    def test_delete_death_launch_with_non_registered_id(self, client):
        response = client.delete("/death_launch/0")

        assert response.status_code == 404
        assert response.json["message"] == "death_launch_not_found"

    def test_delete_death_launch(self, client):
        response = client.delete("/death_launch/1")

        assert response.status_code == 200
        assert response.json["message"] == "death_launch_deleted"

    # --------------------- Helper Functions ---------------------

    def _test_get_death_launch_list_item(self, data: dict[str, any]) -> None:
        assert data["id"] == 1
        assert data["name"] == "Patient social name 1"
        assert data["datetime_of_death"] == "25/08/1989 18:00:00"
        assert data["registration_datetime"] == "25/08/1989 23:40:00"
        assert data["responsible_for_registration"] == "Profissional teste 1"
