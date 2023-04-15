import pytest

from app.main import db
from app.test.seeders import create_base_seed_discharge_conditions


@pytest.fixture(scope="module")
def seed_db(database):
    """Seed the database with test data."""
    return create_base_seed_discharge_conditions(db)


@pytest.mark.usefixtures("seed_db")
class TestDischargeConditionsController:
    def test_get_all_discharge_conditions(self, client):
        response = client.get("/discharge_conditions")
        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 3
        assert response.json["total_pages"] == 1
        assert response.json["items"][0]["name"] == "DISCHARGE CONDITION TESTE 1"
        assert response.json["items"][1]["name"] == "DISCHARGE CONDITION TESTE 2"

    def test_get_discharge_conditions_by_name(self, client):
        response = client.get("/discharge_conditions?name=DISCHARGE CONDITION TESTE 1")
        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 1
        assert response.json["total_pages"] == 1
        assert response.json["items"][0]["name"] == "DISCHARGE CONDITION TESTE 1"

    def test_get_second_page_of_discharge_conditions(self, client):
        response = client.get("/discharge_conditions?page=2")
        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 2
        assert response.json["total_items"] == 3
        assert response.json["total_pages"] == 1
        assert len(response.json["items"]) == 0

    def test_get_discharge_condition(self, client):
        response = client.get("/discharge_conditions/1")
        assert response.status_code == 200
        assert response.json["name"] == "DISCHARGE CONDITION TESTE 1"

    def test_get_discharge_condition_not_found(self, client):
        response = client.get("/discharge_conditions/0")
        assert response.status_code == 404
        assert response.json["message"] == "discharge_condition_not_found"

    #                   --PUT--

    def test_update_discharge_condition_with_existing_name(self, client):
        response = client.put(
            "/discharge_conditions/1",
            json={"name": "DISCHARGE CONDITION TESTE 2"},
        )
        assert response.status_code == 409
        assert "name_in_use" == response.json["message"]

    def test_update_discharge_condition_not_found(self, client):
        response = client.put(
            "/discharge_conditions/0",
            json={"name": "DISCHARGE CONDITION TESTE 0 updated"},
        )
        assert response.status_code == 404
        assert response.json["message"] == "discharge_condition_not_found"

    def test_update_discharge_condition_without_name(self, client):
        response = client.put("/discharge_conditions/1", json={})
        assert response.status_code == 400
        assert "name" in response.json["errors"].keys()

    def test_update_discharge_condition_with_empty_name(self, client):
        response = client.put("/discharge_conditions/1", json={"name": ""})

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert "name" in response.json["errors"].keys()

    def test_update_discharge_condition(self, client):
        response = client.put(
            "/discharge_conditions/1",
            json={"name": "DISCHARGE CONDITION TESTE 1 updated"},
        )
        assert response.status_code == 200
        assert response.json["message"] == "discharge_condition_updated"

    #                   --POST--

    def test_create_discharge_condition_with_existing_name(self, client):
        response = client.post(
            "/discharge_conditions", json={"name": "DISCHARGE CONDITION TESTE 2"}
        )
        assert response.status_code == 409
        assert "name_in_use" == response.json["message"]

    def test_create_discharge_condition_without_name(self, client):
        response = client.post("/discharge_conditions", json={})
        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert "name" in response.json["errors"].keys()

    def test_create_discharge_condition_with_empty_name(self, client):
        response = client.post("/discharge_conditions", json={"name": ""})

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert "name" in response.json["errors"].keys()

    def test_create_discharge_condition(self, client):
        response = client.post(
            "/discharge_conditions", json={"name": "DISCHARGE CONDITION TESTE 4"}
        )
        assert response.status_code == 201
        assert response.json["message"] == "discharge_condition_created"

    #                    --DELETE--

    def test_delete_discharge_condition_not_found(self, client):
        response = client.delete("/discharge_conditions/0")
        assert response.status_code == 404
        assert response.json["message"] == "discharge_condition_not_found"

    def test_delete_discharge_condition(self, client):
        response = client.delete("/discharge_conditions/1")
        assert response.status_code == 200
        assert response.json["message"] == "discharge_condition_deleted"
