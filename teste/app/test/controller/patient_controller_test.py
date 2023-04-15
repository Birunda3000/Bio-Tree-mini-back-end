from datetime import datetime, timedelta

import pytest

from app.main import db
from app.main.service import date_to_string
from app.test.seeders import create_base_seed_patient


@pytest.fixture(scope="module")
def seeded_database(client, database):
    """Seed database with patient data"""
    return create_base_seed_patient(db)


@pytest.mark.usefixtures("seeded_database")
class TestPatientController:

    # --------------------- GET ---------------------
    def test_get_patients(self, client):
        response = client.get("/patient")
        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 11
        assert response.json["total_pages"] == 2
        assert response.json["items"][0]["name"] == "Patient teste 1"
        assert response.json["items"][0]["contact"]["cellphone"] == "85987654321"
        assert response.json["items"][0]["cpf"] == "11545559090"
        assert response.json["items"][0]["cns_cod"] == "867771826050006"
        assert response.json["items"][1]["name"] == "Patient teste 2"
        assert response.json["items"][1]["cpf"] == "10177488026"
        assert response.json["items"][1]["cns_cod"] == "181915807040001"

    def test_get_patients_by_page(self, client):
        response = client.get("/patient", query_string={"page": 2})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert len(response.json["items"]) == 1
        assert response.json["current_page"] == 2

    def test_get_patients_by_cpf(self, client):
        response = client.get("/patient", query_string={"cpf": "11545559090"})
        assert response.status_code == 200
        assert len(response.json) == 4
        assert len(response.json["items"]) == 1
        assert response.json["items"][0]["name"] == "Patient teste 1"
        assert response.json["items"][0]["cns_cod"] == "867771826050006"
        assert response.json["items"][0]["cpf"] == "11545559090"
        assert response.json["current_page"] == 1

    def test_get_patients_by_name(self, client):
        response = client.get("/patient", query_string={"name": "Patient teste 1"})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert len(response.json["items"]) == 3
        assert response.json["items"][0]["cpf"] == "11545559090"
        assert response.json["items"][0]["cns_cod"] == "867771826050006"
        assert response.json["current_page"] == 1

    # --------------------- GET PATIENTS BY ID---------------------

    def test_get_patient_by_invalid_id(self, client):
        response = client.get("/patient/0")

        assert response.status_code == 404
        assert response.json["message"] == "patient_not_found"

    def test_get_patient_by_id(self, client):
        response = client.get("/patient/1")
        assert response.status_code == 200
        assert response.json["id"] == 1
        assert response.json["name"] == "Patient teste 1"

    # --------------------- GET PATIENT  BY NAME ---------------------

    def test_get_patient_by_name(self, client):
        response = client.get("/patient/Patient")

        assert response.status_code == 200
        assert len(response.json) == 11
        assert response.json[0]["id"] == 1
        assert response.json[0]["name"] == "Patient teste 1"

    def test_get_patient_by_short_name(self, client):
        response = client.get("/patient/pa")

        assert response.status_code == 400
        assert "patient_name" in response.json["errors"].keys()

    def test_get_patient_by_exact_name(self, client):
        response = client.get("/patient/Patient%20teste%201")
        assert response.status_code == 200
        assert len(response.json) == 3
        assert response.json[0]["id"] == 1
        assert response.json[0]["name"] == "Patient teste 1"
        assert response.json[1]["id"] == 10
        assert response.json[1]["name"] == "Patient teste 10"
        assert response.json[2]["id"] == 11
        assert response.json[2]["name"] == "Patient teste 11"

    # --------------------- UPDATE ---------------------

    @pytest.mark.parametrize(
        "cpf",
        [
            "00000000000",
            "01234567891",
            "123123",
            "123456789123",
        ],
    )
    def test_update_patient_with_invalid_cpf(self, client, base_patient, cpf):
        base_patient["cpf"] = cpf
        response = client.put("/patient/1", json=base_patient)

        assert response.status_code == 400
        assert "cpf" in response.json["errors"].keys()

    def test_update_patient_with_registered_cpf(self, client, base_patient):
        base_patient["cpf"] = "10177488026"

        response = client.put("/patient/1", json=base_patient)

        assert response.status_code == 409
        assert response.json["message"] == "cpf_in_use"

    def test_update_patient_with_invalid_birthdate(self, client, base_patient):
        next_day_date = (datetime.now() + timedelta(days=1)).date()
        base_patient["birth"] = date_to_string(next_day_date)

        response = client.post("/patient", json=base_patient)

        assert response.status_code == 400
        assert "birth" in response.json["errors"].keys()

    def test_update_patient_with_empty_name(self, client, base_patient):
        base_patient["name"] = ""
        response = client.put("/patient/1", json=base_patient)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert "name" in response.json["errors"].keys()

    def test_update_patient(self, client, base_patient):

        response = client.put("/patient/1", json=base_patient)
        assert response.status_code == 200
        assert response.json["message"] == "patient_updated"

    # --------------------- POST ---------------------

    @pytest.mark.parametrize(
        "cpf",
        [
            "00000000000",
            "01234567891",
            "123123",
            "123456789123",
        ],
    )
    def test_register_patient_with_invalid_cpf(self, client, base_patient, cpf):
        base_patient["cpf"] = cpf

        response = client.post("/patient", json=base_patient)

        assert response.status_code == 400
        assert "cpf" in response.json["errors"].keys()

    def test_register_patient_with_invalid_sex(self, client, base_patient):
        base_patient["sex"] = "sexo_invalido"

        response = client.post("/patient", json=base_patient)

        assert response.status_code == 400
        assert "sex" in response.json["errors"].keys()

    def test_register_patient_with_invalid_gender(self, client, base_patient):
        base_patient["gender"] = "genero_invalido"

        response = client.post("/patient", json=base_patient)

        assert response.status_code == 400
        assert "gender" in response.json["errors"].keys()

    def test_register_patient_with_invalid_breed(self, client, base_patient):
        base_patient["breed"] = "raca_invalida"

        response = client.post("/patient", json=base_patient)

        assert response.status_code == 400
        assert "breed" in response.json["errors"].keys()

    def test_register_patient_with_registered_cpf(self, client, base_patient):
        base_patient["email"] = "patient1@test.com"
        base_patient["cpf"] = "11545559090"

        response = client.post("/patient", json=base_patient)
        assert response.status_code == 409
        assert response.json["message"] == "cpf_in_use"

    def test_register_patient_with_registered_email(self, client, base_patient):
        base_patient["email"] = "patient@test.com"
        response = client.post("/patient", json=base_patient)
        assert response.status_code == 409
        assert response.json["message"] == "email_in_use"

    def test_register_patient_with_invalid_birthdate(self, client, base_patient):
        next_day_date = (datetime.now() + timedelta(days=1)).date()
        base_patient["birth"] = date_to_string(next_day_date)

        response = client.post("/patient", json=base_patient)

        assert response.status_code == 400
        assert "birth" in response.json["errors"].keys()

    def test_register_patient_with_empty_name(self, client, base_patient):
        base_patient["name"] = ""
        response = client.post("/patient", json=base_patient)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert "name" in response.json["errors"].keys()

    def test_register_patient(self, client, base_patient):
        base_patient["cpf"] = "79503481007"
        base_patient["email"] = "patient1@test.com"
        response = client.post("/patient", json=base_patient)

        assert response.json["message"] == "patient_created"
