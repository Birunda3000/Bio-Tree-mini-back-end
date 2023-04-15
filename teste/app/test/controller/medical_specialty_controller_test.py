import pytest

from app.main import db
from app.test.seeders import create_base_seed_medical_specialty


@pytest.fixture(scope="module")
def seeded_database(client, database):
    """Seed database with prescription data"""

    create_base_seed_medical_specialty(db)


@pytest.mark.usefixtures("seeded_database")
class TestMedicalSpecialtyController:

    # --------------------- GET MEDICAL SPECIALTIES ---------------------

    def test_get_medical_specialties(self, client):
        response = client.get("/medical_specialty")

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 3
        assert response.json["total_pages"] == 1
        assert response.json["items"][0]["id"] == 1
        assert response.json["items"][0]["name"] == "MEDICAL SPECIALTY ONE"
        assert response.json["items"][1]["id"] == 2
        assert response.json["items"][1]["name"] == "MEDICAL SPECIALTY TWO"
        assert response.json["items"][2]["id"] == 3
        assert response.json["items"][2]["name"] == "MEDICAL SPECIALTY THREE"

    def test_get_medical_specialties_by_name(self, client):
        response = client.get("/medical_specialty", query_string={"name": "One"})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 1
        assert response.json["total_pages"] == 1
        assert response.json["items"][0]["id"] == 1
        assert response.json["items"][0]["name"] == "MEDICAL SPECIALTY ONE"

    # --------------------- GET MEDICAL SPECIALTY  ---------------------

    def test_get_medical_specialty(self, client):
        response = client.get("/medical_specialty/1")

        assert response.status_code == 200
        assert len(response.json) == 2
        assert response.json["id"] == 1
        assert response.json["name"] == "MEDICAL SPECIALTY ONE"

    def test_get_medical_specialty_that_not_exists(self, client):
        response = client.get("/medical_specialty/0")

        assert response.status_code == 404
        assert response.json["message"] == "medical_specialty_not_found"

    # --------------------- UPDATE MEDICAL SPECIALTY ---------------------

    def test_update_medical_specialty_with_the_same_name(
        self, client, base_medical_specialty
    ):
        base_medical_specialty["name"] = "medical specialty one"
        response = client.put("/medical_specialty/1", json=base_medical_specialty)

        assert response.status_code == 200
        assert response.json["message"] == "medical_specialty_updated"

    def test_update_medical_specialty_with_invalid_input(
        self, client, base_medical_specialty
    ):
        base_medical_specialty["name"] = 0
        response = client.put("/medical_specialty/1", json=base_medical_specialty)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"

    def test_update_medical_specialty_that_not_exists(
        self, client, base_medical_specialty
    ):
        response = client.put("/medical_specialty/0", json=base_medical_specialty)

        assert response.status_code == 404
        assert response.json["message"] == "medical_specialty_not_found"

    def test_update_medical_specialty_with_name_that_already_exists(
        self, client, base_medical_specialty
    ):
        base_medical_specialty["name"] = "medical specialty two"
        response = client.put("/medical_specialty/1", json=base_medical_specialty)

        assert response.status_code == 409
        assert response.json["message"] == "name_in_use"

    def test_update_medical_specialty_with_empty_name(
        self, client, base_medical_specialty
    ):
        base_medical_specialty["name"] = ""
        response = client.put("/medical_specialty/1", json=base_medical_specialty)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert "name" in response.json["errors"].keys()

    def test_update_medical_specialty(self, client, base_medical_specialty):
        base_medical_specialty["name"] = "update"
        response = client.put("/medical_specialty/1", json=base_medical_specialty)

        assert response.status_code == 200
        assert response.json["message"] == "medical_specialty_updated"

    # --------------------- CREATE MEDICAL SPECIALTY ---------------------

    def test_create_medical_specialty_with_invalid_input(
        self, client, base_medical_specialty
    ):
        base_medical_specialty["name"] = 0
        response = client.post("/medical_specialty", json=base_medical_specialty)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"

    def test_create_medical_specialty_with_name_that_already_exists(
        self, client, base_medical_specialty
    ):
        base_medical_specialty["name"] = "medical specialty two"
        response = client.post("/medical_specialty", json=base_medical_specialty)

        assert response.status_code == 409
        assert response.json["message"] == "name_in_use"

    def test_create_medical_specialty_with_empty_name(
        self, client, base_medical_specialty
    ):
        base_medical_specialty["name"] = ""
        response = client.post("/medical_specialty", json=base_medical_specialty)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert "name" in response.json["errors"].keys()

    def test_create_medical_specialty(self, client, base_medical_specialty):
        response = client.post("/medical_specialty", json=base_medical_specialty)

        assert response.status_code == 201
        assert response.json["message"] == "medical_specialty_created"

    # --------------------- DELETE MEDICAL SPECIALTY ---------------------

    def test_delete_prescription_with_non_registered_id(self, client):
        response = client.delete("/medical_specialty/0")

        assert response.status_code == 404
        assert response.json["message"] == "medical_specialty_not_found"

    def test_delete_medical_specialty(self, client):
        response = client.delete("/medical_specialty/1")

        assert response.status_code == 200
        assert response.json["message"] == "medical_specialty_deleted"
