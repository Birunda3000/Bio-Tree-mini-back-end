import pytest

from app.main import db
from app.test.seeders import create_base_seed_medicine


@pytest.fixture(scope="module")
def seeded_database(client, database):
    """Seed database with medicine data"""
    return create_base_seed_medicine(db)


@pytest.mark.usefixtures("seeded_database")
class TestMedicineController:
    def test_get_medicines(self, client):
        response = client.get("/medicine")

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 5
        assert response.json["total_pages"] == 1
        assert response.json["items"][0]["name"] == "Medicine One"
        assert response.json["items"][1]["name"] == "Medicine Two"
        assert response.json["items"][2]["name"] == "Medicine Three"
        assert response.json["items"][3]["name"] == "Medicine Four"
        assert response.json["items"][4]["name"] == "Medicine Five"

    def test_get_medicines_by_page(self, client):
        response = client.get("/medicine", query_string={"page": 2})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert len(response.json["items"]) == 0
        assert response.json["current_page"] == 2

    def test_get_medicine_by_id(self, client):
        response = client.get("/medicine/1")

        assert response.status_code == 200
        assert len(response.json) == 2
        assert response.json["id"] == 1
        assert response.json["name"] == "Medicine One"

    def test_get_medicine_by_invalid_id(self, client):
        response = client.get("/medicine/999")

        assert response.status_code == 404
        assert response.json["message"] == "medicine_not_found"

    def test_update_medicine_without_name(self, client, base_medicine):
        base_medicine["name"] = ""
        response = client.patch("/medicine/1", json=base_medicine)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert "name" in response.json["errors"].keys()

    def test_update_medicine(self, client):
        response = client.patch("/medicine/5", json={"name": "Medicine Test"})
        assert response.status_code == 200
        assert response.json["message"] == "medicine_updated"

    def test_register_medicine_without_name(self, client, base_medicine):
        base_medicine["name"] = ""
        response = client.post("/medicine", json=base_medicine)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert "name" in response.json["errors"].keys()

    def test_register_medicine(self, client, base_medicine):
        response = client.post("/medicine", json=base_medicine)

        assert response.status_code == 201
        assert response.json["message"] == "medicine_created"

    def test_update_medicine_with_invalid_id(self, client):
        response = client.patch("/medicine/999", json={"name": "Medicine Test"})
        assert response.status_code == 404
        assert response.json["message"] == "medicine_not_found"
