import pytest

from app.main import db
from app.test.seeders import create_base_seed_professional, create_base_seed_user


@pytest.fixture(scope="module")
def seeded_database(client, database):
    """Seed database with user data"""

    create_base_seed_professional(db)
    return create_base_seed_user(db)


@pytest.mark.usefixtures("seeded_database")
class TestActivationController:

    # --------------------- GET ---------------------

    def test_check_token_valid(self, client):
        response = client.get("/activation/test")

        assert response.status_code == 200
        assert response.json["message"] == "token_valid"

    def test_check_token_invalid(self, client):
        response = client.get("/activation/testest")

        assert response.status_code == 409
        assert response.json["message"] == "token_invalid"

    def test_check_token_expired(self, client):
        response = client.get("/activation/test8")

        assert response.status_code == 401
        assert response.json["message"] == "token_expired"

    # --------------------- PUT ---------------------

    def test_resend_activation_token_without_user_registered(self, client):
        response = client.put("/activation/resend/10")

        assert response.status_code == 404
        assert response.json["message"] == "user_not_found"

    def test_resend_activation_token_without_professional_registered(self, client):
        response = client.put("/activation/resend/7")

        assert response.json["message"] == "professional_not_found"

    def test_resend_activation_token_with_user_already_activated(self, client):
        response = client.put("/activation/resend/4")

        assert response.status_code == 409
        assert response.json["message"] == "user_already_activated"

    def test_resend_activation_token_with_user_is_blocked(self, client):
        response = client.put("/activation/resend/5")

        assert response.status_code == 409
        assert response.json["message"] == "user_is_blocked"

    def test_resend_activation_token(self, client):
        response = client.put("/activation/resend/1")

        assert response.status_code == 200
        assert response.json["message"] == "activation_email_resent"

    # --------------------- POST ---------------------

    def test_activate_user_not_registered(self, client):
        response = client.post(
            "/activation/testest",
            json={"new_password": "testesteste", "repeat_new_password": "testesteste"},
        )

        assert response.status_code == 409
        assert response.json["message"] == "token_invalid"

    def test_activate_user_with_short_password(self, client):
        response = client.post(
            "/activation/test3",
            json={"new_password": "test", "repeat_new_password": "test"},
        )

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"

    def test_activate_user_with_token_expired(self, client):
        response = client.post(
            "/activation/test5",
            json={"new_password": "testesteste", "repeat_new_password": "testesteste"},
        )

        assert response.status_code == 401
        assert response.json["message"] == "token_expired"

    def test_activate_user_with_different_passwords(self, client):
        response = client.post(
            "/activation/test6",
            json={"new_password": "testesteste", "repeat_new_password": "testestseste"},
        )

        assert response.status_code == 409
        assert response.json["message"] == "passwords_not_match"

    def test_activate_user(self, client):
        response = client.post(
            "/activation/test6",
            json={"new_password": "testesteste", "repeat_new_password": "testesteste"},
        )

        assert response.status_code == 201
        assert response.json["message"] == "user_activated"

    def test_activate_user_with_status_blocked(
        self,
        client,
    ):
        response = client.post(
            "/activation/test4",
            json={"new_password": "testesteste", "repeat_new_password": "testesteste"},
        )

        assert response.status_code == 409
        assert response.json["message"] == "user_is_blocked"

    def test_activate_user_with_user_already_activated(
        self,
        client,
    ):
        response = client.post(
            "/activation/test7",
            json={"new_password": "testesteste", "repeat_new_password": "testesteste"},
        )

        assert response.status_code == 409
        assert response.json["message"] == "user_already_activated"

    def test_activate_user_password_already_created(
        self,
        client,
    ):
        response = client.post(
            "/activation/test2",
            json={"new_password": "testesteste", "repeat_new_password": "testesteste"},
        )

        assert response.status_code == 409
        assert response.json["message"] == "password_already_created"
