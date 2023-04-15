import pytest

from app.main import db
from app.test.seeders import create_base_seed_unit_measurement


@pytest.fixture(scope="module")
def seeded_database(client, database):
    """Seed database with prescription data"""

    create_base_seed_unit_measurement(db)


@pytest.mark.usefixtures("seeded_database")
class TestUnitMeasurementController:

    # --------------------- GET UNIT MEASUREMENTS ---------------------

    def test_get_unit_measurements(self, client):
        response = client.get("/unit_measurement")

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 3
        assert response.json["total_pages"] == 1
        assert response.json["items"][0]["id"] == 1
        assert response.json["items"][0]["name"] == "UNIT MEASUREMENT ONE"
        assert response.json["items"][1]["id"] == 2
        assert response.json["items"][1]["name"] == "UNIT MEASUREMENT TWO"
        assert response.json["items"][2]["id"] == 3
        assert response.json["items"][2]["name"] == "UNIT MEASUREMENT THREE"

    def test_get_unit_measurements_by_name(self, client):
        response = client.get("/unit_measurement", query_string={"name": "One"})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 1
        assert response.json["total_pages"] == 1
        assert response.json["items"][0]["id"] == 1
        assert response.json["items"][0]["name"] == "UNIT MEASUREMENT ONE"

    # --------------------- GET UNIT MEASUREMENT  ---------------------

    def test_get_unit_measurement(self, client):
        response = client.get("/unit_measurement/1")

        assert response.status_code == 200
        assert len(response.json) == 2
        assert response.json["id"] == 1
        assert response.json["name"] == "UNIT MEASUREMENT ONE"

    def test_get_unit_measurement_that_not_exists(self, client):
        response = client.get("/unit_measurement/0")

        assert response.status_code == 404
        assert response.json["message"] == "unit_measurement_not_found"

    # --------------------- UPDATE UNIT MEASUREMENT ---------------------

    def test_update_unit_measurement_with_invalid_data(
        self, client, base_unit_measurement
    ):
        base_unit_measurement["name"] = 0
        response = client.put("/unit_measurement/1", json=base_unit_measurement)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"

    def test_update_unit_measurement_that_not_exists(
        self, client, base_unit_measurement
    ):
        response = client.put("/unit_measurement/0", json=base_unit_measurement)

        assert response.status_code == 404
        assert response.json["message"] == "unit_measurement_not_found"

    def test_update_unit_measurement_with_registered_name(
        self, client, base_unit_measurement
    ):
        base_unit_measurement["name"] = "unit measurement two"
        response = client.put("/unit_measurement/1", json=base_unit_measurement)

        assert response.status_code == 409
        assert response.json["message"] == "name_in_use"

    def test_update_unit_measurement(self, client, base_unit_measurement):
        response = client.put("/unit_measurement/1", json=base_unit_measurement)

        assert response.status_code == 200
        assert response.json["message"] == "unit_measurement_updated"

    # --------------------- CREATE UNIT MEASUREMENT ---------------------

    def test_create_unit_measurement_with_invalid_data(
        self, client, base_unit_measurement
    ):
        base_unit_measurement["name"] = 0
        response = client.post("/unit_measurement", json=base_unit_measurement)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"

    def test_create_unit_measurement_with_registered_name(
        self, client, base_unit_measurement
    ):
        response = client.post("/unit_measurement", json=base_unit_measurement)

        assert response.status_code == 409
        assert response.json["message"] == "name_in_use"

    def test_create_unit_measurement(self, client, base_unit_measurement):

        base_unit_measurement["name"] = "unit measurement one"
        response = client.post("/unit_measurement", json=base_unit_measurement)

        assert response.status_code == 201
        assert response.json["message"] == "unit_measurement_created"

    # --------------------- DELETE UNIT MEASUREMENT ---------------------

    def test_delete_prescription_with_non_registered_id(self, client):
        response = client.delete("/unit_measurement/0")

        assert response.status_code == 404
        assert response.json["message"] == "unit_measurement_not_found"

    def test_delete_unit_measurement(self, client):
        response = client.delete("/unit_measurement/1")

        assert response.status_code == 200
        assert response.json["message"] == "unit_measurement_deleted"
