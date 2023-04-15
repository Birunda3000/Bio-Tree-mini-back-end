import pytest

from app.main import db
from app.test.seeders import (
    create_base_seed_action,
    create_base_seed_prescription,
    create_base_seed_protocol,
)


@pytest.fixture(scope="module")
def seeded_database(client, database):
    """Seed database with action data"""

    create_base_seed_action(db)
    create_base_seed_protocol(db)
    create_base_seed_prescription(db)


@pytest.mark.usefixtures("seeded_database")
class TestActionController:

    # --------------------- GET ACTIONS ---------------------

    def test_get_actions(self, client):
        response = client.get("/action")

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 3
        assert response.json["total_pages"] == 1
        assert response.json["items"][0]["name"] == "AÇÃO TESTE 1"
        assert response.json["items"][1]["name"] == "AÇÃO TESTE 2"

    def test_get_actions_by_page(self, client):
        response = client.get("/action", query_string={"page": 2})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert len(response.json["items"]) == 0
        assert response.json["current_page"] == 2

    @pytest.mark.parametrize(
        "name",
        ["ação teste 1", "1"],
        ids=["complete_name", "incomplete_name"],
    )
    def test_get_action_by_name(self, client, name):
        response = client.get("/action", query_string={"name": name})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["total_items"] == 1
        assert response.json["items"][0]["name"] == "AÇÃO TESTE 1"

    # --------------------- UPDATE ACTION ---------------------

    def test_update_action_with_registered_name(self, client):
        response = client.put("/action/1", json={"name": "ação teste 2"})

        assert response.status_code == 409
        assert response.json["message"] == "name_in_use"

    def test_update_action_without_name(self, client):
        response = client.put("/action/1", json={})

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert "name" in response.json["errors"].keys()

    def test_update_action_with_empty_name(self, client):
        response = client.put("/action/1", json={"name": ""})

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert "name" in response.json["errors"].keys()

    def test_update_action_with_non_registered_id(self, client):
        response = client.put("/action/0", json={"name": "ação teste Atualizada"})

        assert response.status_code == 404
        assert response.json["message"] == "action_not_found"

    def test_update_action(self, client):
        response = client.put("/action/1", json={"name": "ação teste Atualizada"})

        assert response.status_code == 200
        assert response.json["message"] == "action_updated"

    # --------------------- CREATE ACTION ---------------------

    def test_create_action_with_registered_name(self, client):
        response = client.post("/action", json={"name": "ação teste 2"})

        assert response.status_code == 409
        assert response.json["message"] == "name_in_use"

    def test_create_action_without_name(self, client):
        response = client.post("/action", json={})

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert "name" in response.json["errors"].keys()

    def test_create_action_with_empty_name(self, client):
        response = client.post("/action", json={"name": ""})

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert "name" in response.json["errors"].keys()

    def test_create_action(self, client):
        response = client.post("/action", json={"name": "ação teste"})

        assert response.status_code == 201
        assert response.json["message"] == "action_created"

    # --------------------- DELETE ACTION ---------------------

    def test_delete_action_with_non_registered_id(self, client):
        response = client.delete("/action/0")

        assert response.status_code == 404
        assert response.json["message"] == "action_not_found"

    def test_delete_action_associated_with_prescription(self, client):
        response = client.delete("/action/1")

        assert response.status_code == 409
        assert response.json["message"] == "action_is_associated_with_prescription"

    def test_delete_action(self, client):
        response = client.delete("/action/2")

        assert response.status_code == 200
        assert response.json["message"] == "action_deleted"
