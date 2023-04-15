import pytest

from app.main import db
from app.test.seeders import create_base_seed_professional, create_base_seed_user


@pytest.fixture(scope="module")
def seeded_database(client, database):
    """Seed database with user data"""

    create_base_seed_professional(db)
    return create_base_seed_user(db)


@pytest.mark.usefixtures("seeded_database")
class TestLoginController:
    def test_user_login(self, client):
        response = client.post(
            "/login", json={"login": "user1@uece.br", "password": "bbbbbbbbb"}
        )

        assert response.status_code == 200
        assert response.json["professional_name"] == "Profissional teste 2"

    def test_user_login_with_wrong_password(self, client):
        response = client.post(
            "/login", json={"login": "user1@uece.br", "password": "12345678"}
        )

        assert response.status_code == 401
        assert response.json["message"] == "password_incorrect_information"

    def test_user_login_with_invalid_login(self, client):
        response = client.post("/login", json={"login": "user", "password": "12345678"})

        assert response.status_code == 401
        assert response.json["message"] == "password_incorrect_information"

    def test_user_login_with_user_not_activated(self, client):
        response = client.post(
            "/login", json={"login": "user@uece.br", "password": "aaaaaaaaa"}
        )

        assert response.status_code == 409
        assert response.json["message"] == "user_not_activated"

    def test_user_login_without_a_valid_professional(self, client):
        response = client.post(
            "/login", json={"login": "user7@uece.br", "password": "testeteste"}
        )

        assert response.status_code == 404
        assert response.json["message"] == "professional_not_found"
