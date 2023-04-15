import pytest

from app.main import db
from app.test.seeders import (
    create_base_seed_admission,
    create_base_seed_bed,
    create_base_seed_patient,
    create_base_seed_professional,
    create_base_seed_queue_manager,
)


@pytest.fixture(scope="module")
def seeded_database(client, database):
    """Seed database with admission data"""
    create_base_seed_bed(db)
    create_base_seed_patient(db)
    create_base_seed_professional(db)
    create_base_seed_queue_manager(db)
    create_base_seed_admission(db)


@pytest.mark.usefixtures("seeded_database")
class TestAdmissionController:

    # --------------------- GET ADMISSION ---------------------

    def test_get_admission(self, client):
        response = client.get("/admission")

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 2
        assert response.json["total_pages"] == 1

        assert response.json["items"][0]["id"] == 1
        assert response.json["items"][0]["professional_id"] == 1
        assert response.json["items"][0]["patient_id"] == 1
        assert response.json["items"][0]["bed"]["id"] == 1
        assert response.json["items"][0]["type"] == "Observação"
        assert response.json["items"][1]["id"] == 2
        assert response.json["items"][1]["professional_id"] == 2
        assert response.json["items"][1]["patient_id"] == 2
        assert response.json["items"][1]["bed"]["id"] == 5
        assert response.json["items"][1]["type"] == "Internação"

    def test_get_admission_by_page(self, client):
        response = client.get("/admission", query_string={"page": 2})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert len(response.json["items"]) == 0
        assert response.json["current_page"] == 2

    @pytest.mark.parametrize(
        "key, value, total_items",
        [
            ("page", 1, 2),
            ("patient_id", 1, 1),
            ("professional_id", 1, 1),
            ("bed_id", 1, 1),
            ("type", "Observação", 2),
        ],
    )
    def test_get_admission_by(self, client, key, value, total_items):
        response = client.get("/admission", query_string={key: value})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["total_items"] == total_items

    # --------------------- CREATE ADMISSION ---------------------

    def test_create_admission(self, client, base_admission):
        response = client.post("/admission", json=base_admission)

        assert response.status_code == 201
        assert response.json["message"] == "patient_admitted"

    @pytest.mark.parametrize(
        "key,new_value,expected_message",
        [
            ("patient_id", 0, "patient_not_found"),
            ("professional_id", 0, "professional_not_found"),
            ("bed_id", 0, "bed_not_found"),
        ],
        ids=[
            "invalid_patient_id",
            "invalid_professional_id",
            "invalid_bed_id",
        ],
    )
    def test_create_admission_with_invalid_data(
        self, client, base_admission, key, new_value, expected_message
    ):
        base_admission[key] = new_value

        response = client.post("/admission", json=base_admission)

        assert response.status_code == 404
        assert response.json["message"] == expected_message

    @pytest.mark.parametrize(
        "key_popped",
        ["professional_id", "patient_id", "bed_id"],
        ids=[
            "without_professional_id",
            "without_patient_id",
            "without_bed_id",
        ],
    )
    def test_create_admission_without_required_data(
        self, client, base_admission, key_popped
    ):
        base_admission.pop(key_popped, None)

        response = client.post("/admission", json=base_admission)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert key_popped in response.json["errors"].keys()

    def test_create_admission_with_not_available_bed(self, client, base_admission):
        base_admission["bed_id"] = 4
        response = client.post("/admission", json=base_admission)

        assert response.status_code == 409
        assert response.json["message"] == "bed_not_available"

    def test_create_admission_with_patient_not_in_queue(self, client, base_admission):
        base_admission["patient_id"] = 5
        response = client.post("/admission", json=base_admission)

        assert response.status_code == 409
        assert response.json["message"] == "patient_not_in_queue"
