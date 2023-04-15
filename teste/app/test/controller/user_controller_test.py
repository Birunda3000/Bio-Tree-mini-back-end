import pytest

from app.main import db
from app.test.seeders import create_base_seed_professional, create_base_seed_user


@pytest.fixture(scope="module")
def seeded_database(client, database):
    """Seed database with user data"""

    create_base_seed_professional(db)
    return create_base_seed_user(db)


@pytest.mark.usefixtures("seeded_database")
class TestUserController:
    def test_get_users(self, client):
        response = client.get("/user")

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 9
        assert response.json["total_pages"] == 1
        assert response.json["items"][0]["professional_id"] == 1
        assert response.json["items"][0]["login"] == "user@uece.br"
        assert response.json["items"][0]["status"] == "waitActivation"
        assert response.json["items"][1]["professional_id"] == 2
        assert response.json["items"][1]["login"] == "user1@uece.br"
        assert response.json["items"][1]["status"] == "active"
        assert response.json["items"][2]["professional_id"] == 10
        assert response.json["items"][2]["login"] == "user2@uece.br"
        assert response.json["items"][2]["status"] == "waitActivation"

    def test_get_users_by_page(self, client):
        response = client.get("/user", query_string={"page": 2})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert len(response.json["items"]) == 0
        assert response.json["current_page"] == 2

    def test_get_user_by_id(self, client):
        response = client.get("/user/1")

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["id"] == 1
        assert response.json["professional_id"] == 1
        assert response.json["login"] == "user@uece.br"
        assert response.json["status"] == "waitActivation"

    def test_get_user_by_invalid_id(self, client):
        response = client.get("/user/999")

        assert response.status_code == 404
        assert response.json["message"] == "user_not_found"

    def test_update_user_with_invalid_status(self, client):
        response = client.patch("/user/1", json={"status": "unknown"})
        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert "status" in response.json["errors"].keys()

    def test_update_user_with_invalid_id(self, client):
        response = client.patch("/user/999", json={"status": "active"})
        assert response.status_code == 404
        assert response.json["message"] == "user_not_found"

    def test_update_user_with_user_never_activated(self, client):
        response = client.patch("/user/1", json={"status": "active"})
        assert response.status_code == 409
        assert response.json["message"] == "user_never_activated"

    def test_update_user_with_unauthorized_status(self, client):
        response = client.patch("/user/2", json={"status": "waitActivation"})
        assert response.json["message"] == "Input payload validation failed"
        assert "status" in response.json["errors"].keys()

    def test_update_user_status(self, client):
        response = client.patch("/user/5", json={"status": "active"})
        assert response.status_code == 200
        assert response.json["message"] == "user_updated"

    def test_register_user_with_invalid_professional(self, client, base_user):
        base_user["professional_id"] = 0
        response = client.post("/user", json=base_user)
        assert response.status_code == 404
        assert response.json["message"] == "professional_not_found"

    def test_register_user_with_registered_login(self, client, base_user):
        base_user["login"] = "user@uece.br"
        response = client.post("/user", json=base_user)
        assert response.status_code == 409
        assert response.json["message"] == "username_in_use"

    def test_register_user(self, client, base_user):
        response = client.post("/user", json=base_user)

        assert response.status_code == 201
        assert response.json["message"] == "user_created"
