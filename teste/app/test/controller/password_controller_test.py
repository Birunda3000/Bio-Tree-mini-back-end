import pytest

from app.main import db
from app.test.seeders import create_base_seed_professional, create_base_seed_user


@pytest.fixture(scope="module")
def seeded_database(client, database):
    """Seed database with user data"""

    create_base_seed_professional(db)
    return create_base_seed_user(db)


@pytest.mark.usefixtures("seeded_database")
class TestPasswordController:

    # ---------------- Check reset password token ----------------

    def test_check_valid_token(self, client):
        response = client.get("/password/redefine/test")

        assert response.status_code == 200
        assert response.json["message"] == "token_valid"

    def test_check_expired_token(self, client):
        response = client.get("/password/redefine/test3")

        assert response.status_code == 401
        assert response.json["message"] == "token_expired"

    def test_check_token_from_user_not_registered(self, client):
        response = client.get("/password/redefine/test999")

        assert response.status_code == 409
        assert response.json["message"] == "token_invalid"

    # ---------------- Change password when logged in ----------------

    def test_change_password(self, client):
        response = client.patch(
            "/password/change/2",
            json={
                "current_password": "bbbbbbbbb",
                "new_password": "123456789",
                "repeat_new_password": "123456789",
            },
        )

        assert response.status_code == 200
        assert response.json["message"] == "password_updated"

    def test_change_password_with_distinct_passwords(self, client):
        response = client.patch(
            "/password/change/2",
            json={
                "current_password": "bbbbbbbbb",
                "new_password": "123456789",
                "repeat_new_password": "987654321",
            },
        )

        assert response.status_code == 409
        assert response.json["message"] == "passwords_not_match"

    def test_change_password_with_invalid_user(self, client):
        response = client.patch(
            "/password/change/999",
            json={
                "current_password": "aaaaaaaaa",
                "new_password": "123456789",
                "repeat_new_password": "123456789",
            },
        )

        assert response.status_code == 404
        assert response.json["message"] == "user_not_found"

    # ---------------- Redefine password ----------------

    def test_redefine_password_with_expired_token(self, client):
        response = client.patch(
            "/password/redefine/test8",
            json={"new_password": "testesteste", "repeat_new_password": "testesteste"},
        )

        assert response.status_code == 401
        assert response.json["message"] == "token_expired"

    def test_redefine_password_with_user_not_registered(self, client):
        response = client.patch(
            "/password/redefine/test999",
            json={"new_password": "testesteste", "repeat_new_password": "testesteste"},
        )

        assert response.status_code == 409
        assert response.json["message"] == "token_invalid"

    def test_redefine_password_with_user_not_activated(self, client):
        response = client.patch(
            "/password/redefine/test",
            json={"new_password": "testesteste", "repeat_new_password": "testesteste"},
        )

        assert response.status_code == 409
        assert response.json["message"] == "user_not_active"

    def test_redefine_password_with_different_passwords(self, client):
        response = client.patch(
            "/password/redefine/test1",
            json={"new_password": "testesteste", "repeat_new_password": "testestestet"},
        )

        assert response.status_code == 409
        assert response.json["message"] == "passwords_not_match"

    def test_redefine_password_with_short_password(self, client):
        response = client.patch(
            "/password/redefine/test",
            json={"new_password": "teste", "repeat_new_password": "teste"},
        )

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"

    def test_redefine_password_sucess(self, client):
        response = client.patch(
            "/password/redefine/test1",
            json={
                "new_password": "testestestes",
                "repeat_new_password": "testestestes",
            },
        )

        assert response.status_code == 200
        assert response.json["message"] == "password_updated"

    # ---------------- Get recovery email ----------------

    def test_recovery_sucess(self, client):
        response = client.post(
            "/password/forgot", json={"email": "profissional2@uece.com"}
        )

        assert response.status_code == 200
        assert response.json["message"] == "recovery_email_sent"

    def test_recovery_with_invalid_email(self, client):
        response = client.post("/password/forgot", json={"email": "teste.com"})

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"

    def test_recovery_with_professional_not_registered(self, client):
        response = client.post(
            "/password/forgot", json={"email": "teste999@hotmail.com"}
        )

        assert response.status_code == 404
        assert response.json["message"] == "professional_not_found"

    def test_recovery_with_user_not_created(self, client):
        response = client.post(
            "/password/forgot", json={"email": "profissional3@uece.com"}
        )

        assert response.status_code == 404
        assert response.json["message"] == "user_not_found"

    def test_recovery_with_user_not_activated(self, client):
        response = client.post(
            "/password/forgot", json={"email": "profissional1@uece.com"}
        )

        assert response.status_code == 409
        assert response.json["message"] == "user_not_actived"
