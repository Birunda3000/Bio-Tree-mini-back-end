from datetime import datetime, timedelta

import pytest

from app.main import db
from app.main.service import (
    activate_professional,
    date_to_string,
    inactivate_professional,
)
from app.test.seeders import create_base_seed_professional


@pytest.fixture(scope="module")
def seeded_database(database):
    """Seed database with professional data"""
    return create_base_seed_professional(db)


@pytest.mark.usefixtures("seeded_database")
class TestProfessionalController:

    # --------------------- GET PROFESSIONALS ---------------------

    def test_get_professionals(self, client):
        response = client.get("/professional")

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 3
        assert response.json["total_pages"] == 1
        assert response.json["items"][0]["email"] == "profissional1@uece.com"
        assert response.json["items"][0]["cpf"] == "11545559090"
        assert response.json["items"][1]["email"] == "profissional2@uece.com"
        assert response.json["items"][1]["cpf"] == "10177488026"

    def test_get_professionals_by_page(self, client):
        response = client.get("/professional", query_string={"page": 2})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert len(response.json["items"]) == 0
        assert response.json["current_page"] == 2

    @pytest.mark.parametrize(
        "cpf", ["10177488026", "101774"], ids=["complete_cpf", "incomplete_cpf"]
    )
    def test_get_professionals_by_cpf(self, client, cpf):
        response = client.get("/professional", query_string={"cpf": cpf})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert len(response.json["items"]) == 1
        assert response.json["items"][0]["email"] == "profissional2@uece.com"
        assert response.json["items"][0]["cpf"] == "10177488026"
        assert response.json["current_page"] == 1

    def test_get_professionals_by_email(self, client):
        response = client.get(
            "/professional", query_string={"email": "profissional2@uece.com"}
        )

        assert response.status_code == 200
        assert len(response.json) == 4
        assert len(response.json["items"]) == 1
        assert response.json["items"][0]["email"] == "profissional2@uece.com"
        assert response.json["items"][0]["cpf"] == "10177488026"
        assert response.json["current_page"] == 1

    def test_get_professionals_by_name(self, client):
        response = client.get(
            "/professional", query_string={"name": "Profissional teste 1"}
        )

        assert response.status_code == 200
        assert len(response.json) == 4
        assert len(response.json["items"]) == 1
        assert response.json["items"][0]["email"] == "profissional1@uece.com"
        assert response.json["items"][0]["cpf"] == "11545559090"
        assert response.json["current_page"] == 1

    def test_get_professionals_by_social_name(self, client):
        response = client.get(
            "/professional",
            query_string={"social_name": "Profissional teste 1 nome social"},
        )

        assert response.status_code == 200
        assert len(response.json) == 4
        assert len(response.json["items"]) == 1
        assert response.json["items"][0]["email"] == "profissional1@uece.com"
        assert response.json["items"][0]["cpf"] == "11545559090"
        assert response.json["current_page"] == 1

    @pytest.mark.parametrize(
        "cns_cod",
        ["867771826050006", "8677718"],
        ids=["complete_cns_cod", "incomplete_cns_cod"],
    )
    def test_get_professionals_by_cns_cod(self, client, cns_cod):
        response = client.get("/professional", query_string={"cns_cod": cns_cod})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert len(response.json["items"]) == 1
        assert response.json["items"][0]["email"] == "profissional1@uece.com"
        assert response.json["items"][0]["cpf"] == "11545559090"
        assert response.json["current_page"] == 1

    def test_get_inactivated_professionals(self, client, base_professional_dismissal):
        inactivate_professional(1, base_professional_dismissal)
        inactivate_professional(2, base_professional_dismissal)
        inactivate_professional(3, base_professional_dismissal)

        response = client.get("/professional")
        assert response.status_code == 200
        assert len(response.json) == 4
        assert len(response.json["items"]) == 0

        activate_professional(1)
        activate_professional(2)
        activate_professional(3)

    # --------------------- GET PROFESSIONALS BY ID ---------------------

    def test_get_professional_by_id(self, client):
        response = client.get("/professional/1")
        assert response.status_code == 200
        assert response.json["id"] == 1
        assert response.json["name"] == "Profissional teste 1"

    def test_get_inactivated_professional_by_id(self, client, base_professional_dismissal):
        inactivate_professional(1, base_professional_dismissal)

        response = client.get("/professional/1")

        assert response.status_code == 409
        assert response.json["message"] == "professional_is_inactive"

        activate_professional(1)

    def test_get_professional_by_invalid_id(self, client):
        response = client.get("/professional/0")

        assert response.status_code == 404
        assert response.json["message"] == "professional_not_found"

    # --------------------- GET PROFESSIONAL  BY NAME ---------------------

    def test_get_professional_by_name(self, client):
        response = client.get("/professional/profissional")

        assert response.status_code == 200
        assert len(response.json) == 3
        assert response.json[0]["id"] == 1
        assert response.json[0]["name"] == "Profissional teste 1"
        assert response.json[0]["social_name"] == "Profissional teste 1 nome social"

    def test_get_professional_by_short_name(self, client):
        response = client.get("/professional/pr")

        assert response.status_code == 400
        assert "professional_name" in response.json["errors"].keys()

    def test_get_professional_by_exact_name(self, client):
        response = client.get("/professional/Profissional%20teste%201")

        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]["id"] == 1
        assert response.json[0]["name"] == "Profissional teste 1"

    def test_get_inactivated_professional_by_name(self, client, base_professional_dismissal):
        inactivate_professional(1, base_professional_dismissal)
        inactivate_professional(2, base_professional_dismissal)
        inactivate_professional(3, base_professional_dismissal)

        response = client.get("/professional/Profissional")

        assert response.status_code == 200
        assert len(response.json) == 0

        activate_professional(1)
        activate_professional(2)
        activate_professional(3)

    # --------------------- UPDATE ---------------------

    @pytest.mark.parametrize(
        "cpf",
        [
            "872.223.780-14",
            "872.2237801",
            "8722237801400",
            "01234567891",
            "87222378014a",
        ],
    )
    def test_update_professional_with_invalid_cpf(self, client, base_professional, cpf):
        base_professional["cpf"] = cpf
        response = client.put("/professional/1", json=base_professional)

        assert response.status_code == 400
        assert "cpf" in response.json["errors"].keys()

    @pytest.mark.parametrize(
        "email", ["email", "email@", "@uece.com", "email @uece.com", "email.@uece.com"]
    )
    def test_update_professional_with_invalid_email(
        self, client, base_professional, email
    ):
        base_professional["email"] = email

        response = client.put("/professional/1", json=base_professional)

        assert response.status_code == 400
        assert "email" in response.json["errors"].keys()

    def test_update_professional_with_invalid_sex(self, client, base_professional):
        base_professional["sex"] = "sexo_invalido"

        response = client.put("/professional/1", json=base_professional)

        assert response.status_code == 400
        assert "sex" in response.json["errors"].keys()

    @pytest.mark.parametrize(
        "cns",
        [
            "1801665484700051",
            "18016654847000",
        ],
    )
    def test_update_professional_with_invalid_cns(self, client, base_professional, cns):
        base_professional["cns_cod"] = cns

        response = client.put("/professional/1", json=base_professional)

        assert response.status_code == 400
        assert "cns_cod" in response.json["errors"].keys()

    @pytest.mark.parametrize(
        "cep",
        [
            "68911-466",
            "6891466",
        ],
    )
    def test_update_professional_with_invalid_cep(self, client, base_professional, cep):
        base_professional["address"]["cep"] = cep

        response = client.put("/professional/1", json=base_professional)

        assert response.status_code == 400
        assert "address.cep" in response.json["errors"].keys()

    def test_update_professional_with_cpf_already_in_use(
        self, client, base_professional
    ):
        base_professional["cpf"] = "10177488026"

        response = client.put("/professional/1", json=base_professional)

        assert response.status_code == 409
        assert response.json["message"] == "cpf_in_use"

    def test_update_professional_with_email_already_in_use(
        self, client, base_professional
    ):
        base_professional["email"] = "profissional1@uece.com"

        response = client.put("/professional/2", json=base_professional)

        assert response.status_code == 409
        assert response.json["message"] == "email_in_use"

    def test_update_professional_with_invalid_birthdate(
        self, client, base_professional
    ):
        next_day_date = (datetime.now() + timedelta(days=1)).date()
        base_professional["birth"] = date_to_string(next_day_date)

        response = client.put("/professional/1", json=base_professional)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert "birth" in response.json["errors"].keys()

    def test_update_professional_with_empty_name(self, client, base_professional):
        base_professional["name"] = None
        response = client.put("/professional/1", json=base_professional)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert "name" in response.json["errors"].keys()

    def test_update_professional(self, client, base_professional):

        response = client.put("/professional/1", json=base_professional)

        assert response.status_code == 200
        assert response.json["message"] == "professional_updated"

    @pytest.mark.parametrize(
        "non_required_data",
        [
            "father_name",
            "cns_cod",
        ],
    )
    def test_update_professional_without_non_required_data(
        self, client, base_professional, non_required_data
    ):
        del base_professional[non_required_data]

        response = client.put("/professional/1", json=base_professional)

        assert response.status_code == 200
        assert response.json["message"] == "professional_updated"

    # --------------------- INACTIVATE PROFESSIONAL ---------------------

    def test_inactivate_professional_with_invalid_id(self, client, base_professional_dismissal):
        response = client.patch("/professional/inactivate/0",json=base_professional_dismissal)
        assert response.status_code == 404
        assert response.json["message"] == "professional_not_found"

    def test_inactivate_professional_already_inactivated(self, client, base_professional_dismissal):
        inactivate_professional(1, base_professional_dismissal)

        response = client.patch("/professional/inactivate/1",json=base_professional_dismissal)
        assert response.status_code == 409
        assert response.json["message"] == "professional_is_inactive"

        activate_professional(1)

    def test_inactivate_professional(self, client, base_professional_dismissal):
        response = client.patch("/professional/inactivate/1",json=base_professional_dismissal)
        assert response.status_code == 200
        assert response.json["message"] == "professional_inactivated"

        activate_professional(1)

    # --------------------- ACTIVATE PROFESSIONAL ---------------------

    def test_activate_professional_with_invalid_id(self, client):
        response = client.patch("/professional/activate/0")
        assert response.status_code == 404
        assert response.json["message"] == "professional_not_found"

    def test_activate_professional_already_activated(self, client):
        response = client.patch("/professional/activate/1")
        assert response.status_code == 409
        assert response.json["message"] == "professional_is_active"

    def test_activate_professional(self, client, base_professional_dismissal):
        inactivate_professional(1, base_professional_dismissal)

        response = client.patch("/professional/activate/1")
        assert response.status_code == 200
        assert response.json["message"] == "professional_activated"

    # --------------------- POST ---------------------

    @pytest.mark.parametrize(
        "email", ["email", "email@", "@uece.com", "email @uece.com", "email.@uece.com"]
    )
    def test_register_professional_with_invalid_email(
        self, client, base_professional, email
    ):
        base_professional["email"] = email

        response = client.post("/professional", json=base_professional)

        assert response.status_code == 400
        assert "email" in response.json["errors"].keys()

    @pytest.mark.parametrize(
        "cpf",
        [
            "872.223.780-14",
            "872.2237801",
            "8722237801400",
            "01234567891",
            "87222378014a",
        ],
    )
    def test_register_professional_with_invalid_cpf(
        self, client, base_professional, cpf
    ):
        base_professional["cpf"] = cpf

        response = client.post("/professional", json=base_professional)

        assert response.status_code == 400
        assert "cpf" in response.json["errors"].keys()

    def test_register_professional_with_invalid_sex(self, client, base_professional):
        base_professional["sex"] = "sexo_invalido"

        response = client.post("/professional", json=base_professional)

        assert response.status_code == 400
        assert "sex" in response.json["errors"].keys()

    @pytest.mark.parametrize(
        "cns",
        [
            "1801665484700051",
            "18016654847000",
        ],
    )
    def test_register_professional_with_invalid_cns(
        self, client, base_professional, cns
    ):
        base_professional["cns_cod"] = cns

        response = client.post("/professional", json=base_professional)

        assert response.status_code == 400
        assert "cns_cod" in response.json["errors"].keys()

    @pytest.mark.parametrize(
        "cep",
        [
            "68911-466",
            "6891466",
        ],
    )
    def test_register_professional_with_invalid_cep(
        self, client, base_professional, cep
    ):
        base_professional["address"]["cep"] = cep

        response = client.post("/professional", json=base_professional)

        assert response.status_code == 400
        assert "address.cep" in response.json["errors"].keys()

    def test_register_professional_with_registered_cpf(self, client, base_professional):
        base_professional["email"] = "profissional@uece.com"

        response = client.post("/professional", json=base_professional)

        assert response.status_code == 409
        assert response.json["message"] == "cpf_in_use"

    def test_register_professional_with_registered_email(
        self, client, base_professional
    ):
        base_professional["email"] = "profissional2@uece.com"
        base_professional["cpf"] = "64756722032"

        response = client.post("/professional", json=base_professional)

        assert response.status_code == 409
        assert response.json["message"] == "email_in_use"

    def test_register_professional_with_invalid_birthdate(
        self, client, base_professional
    ):
        next_day_date = (datetime.now() + timedelta(days=1)).date()
        base_professional["birth"] = date_to_string(next_day_date)

        response = client.post("/professional", json=base_professional)

        assert response.status_code == 400
        assert "birth" in response.json["errors"].keys()

    def test_register_professional_with_empty_name(self, client, base_professional):
        base_professional["name"] = None
        response = client.post("/professional", json=base_professional)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert "name" in response.json["errors"].keys()

    def test_register_professional(self, client, base_professional):

        base_professional["email"] = "profissional@uece.com"
        base_professional["cpf"] = "65435284007"
        response = client.post("/professional", json=base_professional)

        assert response.status_code == 201
        assert response.json["message"] == "professional_created"

    @pytest.mark.parametrize(
        "non_required_data, email, cpf",
        [
            ("father_name", "profissional998@uece.com", "15097246055"),
            ("cns_cod", "profissional999@uece.com", "31179507029"),
        ],
    )
    def test_register_professional_without_non_required_data(
        self, client, base_professional, non_required_data, email, cpf
    ):
        del base_professional[non_required_data]
        base_professional["email"] = email
        base_professional["cpf"] = cpf

        response = client.post("/professional", json=base_professional)

        assert response.status_code == 201
        assert response.json["message"] == "professional_created"
