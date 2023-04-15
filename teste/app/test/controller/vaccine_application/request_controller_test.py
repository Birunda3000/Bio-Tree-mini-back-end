import pytest

from app.main import db
from app.test.seeders import (
    create_base_seed_patient,
    create_base_seed_professional,
    create_base_seed_queue_manager,
    create_base_seed_risk_classification,
    create_base_seed_vaccine,
    create_base_seed_vaccine_application,
    create_base_seed_vaccine_application_request,
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
    create_base_seed_vaccine_application_request(db)


@pytest.mark.usefixtures("seeded_database")
class TestVaccineApplicationRequestController:

    # --------------------- GET ---------------------

    def test_get_vaccine_application_request(self, client):
        response = client.get("/vaccine_application_request")

        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 2
        assert response.json["total_pages"] == 1

        assert response.json["items"][0]["id"] == 1
        assert len(response.json["items"][0]["professional"]) == 2
        assert len(response.json["items"][0]["patient"]) == 2
        assert len(response.json["items"][0]["vaccine"]) == 1
        assert response.json["items"][0]["status"] == "Em aguardo"

        assert response.json["items"][1]["id"] == 2
        assert len(response.json["items"][1]["professional"]) == 2
        assert len(response.json["items"][1]["patient"]) == 2
        assert len(response.json["items"][1]["vaccine"]) == 1
        assert response.json["items"][1]["status"] == "Cancelada"

        assert response.status_code == 200

    def test_get_vaccine_application_request_by_page(self, client):
        response = client.get("/vaccine_application_request", query_string={"page": 2})

        assert len(response.json) == 4
        assert len(response.json["items"]) == 0
        assert response.json["current_page"] == 2
        assert response.status_code == 200

    @pytest.mark.parametrize(
        "key, value, total_items",
        [
            ("professional_name", "profissional", 2),
            ("patient_id", 1, 1),
            ("patient_name", "patient social name 1", 1),
            ("vaccine_name", "vacina", 2),
            ("status", "Em aguardo", 1),
            ("status", "Cancelada", 1),
            ("status", "Realizada", 0),
        ],
        ids=[
            "professional_name",
            "patient_id",
            "patient_name",
            "vaccine_name",
            "status_1",
            "status_2",
            "status_3",
        ],
    )
    def test_get_vaccine_application_request_by(self, client, key, value, total_items):
        response = client.get("/vaccine_application_request", query_string={key: value})

        assert len(response.json) == 4
        assert response.json["total_items"] == total_items
        assert response.status_code == 200

    # --------------------- PATCH ---------------------

    def test_update_vaccine_application_request_with_invalid_id(
        self, client, base_vaccine_application_request
    ):
        response = client.patch(
            "/vaccine_application_request/0",
            json=base_vaccine_application_request,
        )

        assert response.json["message"] == "vaccine_application_request_not_found"
        assert response.status_code == 404

    def test_update_vaccine_application_already_canceled(
        self, client, base_vaccine_application_request
    ):
        response = client.patch(
            "/vaccine_application_request/2",
            json=base_vaccine_application_request,
        )

        assert (
            response.json["message"] == "vaccine_application_request_already_canceled"
        )

        assert response.status_code == 409

    def test_update_vaccine_application_request(
        self, client, base_vaccine_application_request
    ):

        response = client.patch(
            "/vaccine_application_request/1",
            json=base_vaccine_application_request,
        )

        assert response.json["message"] == "vaccine_application_request_canceled"
        assert response.status_code == 200

    # --------------------- POST ---------------------

    @pytest.mark.parametrize(
        "key_popped",
        [
            "professional_id",
            "patient_id",
            "vaccine_id",
        ],
        ids=[
            "without_professional_id",
            "without_patient_id",
            "without_vaccine_id",
        ],
    )
    def test_create_vaccine_application_request_without_required_data(
        self, client, base_vaccine_application_request, key_popped
    ):
        base_vaccine_application_request.pop(key_popped, None)

        response = client.post(
            "/vaccine_application_request",
            json=base_vaccine_application_request,
        )

        assert response.json["message"] == "Input payload validation failed"
        assert key_popped in response.json["errors"].keys()
        assert response.status_code == 400

    @pytest.mark.parametrize(
        "key,new_value,expected_message",
        [
            ("patient_id", 0, "patient_not_found"),
            ("professional_id", 0, "professional_not_found"),
            ("vaccine_id", 0, "vaccine_not_found"),
        ],
        ids=[
            "invalid_patient_id",
            "invalid_professional_id",
            "invalid_vaccine_id",
        ],
    )
    def test_create_vaccine_application_request_with_invalid_data(
        self,
        client,
        base_vaccine_application_request,
        key,
        new_value,
        expected_message,
    ):
        base_vaccine_application_request[key] = new_value

        response = client.post(
            "/vaccine_application_request",
            json=base_vaccine_application_request,
        )

        assert response.json["message"] == expected_message
        assert response.status_code == 404

    @pytest.mark.parametrize(
        "key,patient_id",
        [
            ("queue_manager", 10),
            ("risk_classification", 7),
        ],
        ids=[
            "without_queue_manager",
            "without_risk_classification",
        ],
    )
    def test_create_vaccine_application_without_needed_requirements(
        self, client, base_vaccine_application_request, key, patient_id
    ):
        base_vaccine_application_request["patient_id"] = patient_id

        response = client.post(
            "/vaccine_application_request",
            json=base_vaccine_application_request,
        )

        assert response.json["message"] == f"{key}_not_found"
        assert response.status_code == 404

    def test_create_vaccine_application_request(
        self, client, base_vaccine_application_request
    ):
        response = client.post(
            "/vaccine_application_request",
            json=base_vaccine_application_request,
        )

        assert response.json["message"] == "vaccine_application_request_created"
        assert response.status_code == 201
