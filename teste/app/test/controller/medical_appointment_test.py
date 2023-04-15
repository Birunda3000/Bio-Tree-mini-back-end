import pytest

from app.main import db
from app.test.seeders import (
    create_base_seed_patient,
    create_base_seed_professional,
    create_medical_appointment,
)


@pytest.fixture(scope="module")
def seeded_database(client, database):
    """Seed database with medical appointment controller data"""

    create_base_seed_professional(db)
    create_base_seed_patient(db)

    return create_medical_appointment(db)


@pytest.mark.usefixtures("seeded_database")
class TestMedicalAppointmentController:

    # --------------------- GET ---------------------
    def test_get_medical_appointement(self, client):
        response = client.get("/appointment/1")
        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["items"][0]["patient_id"] == 1
        assert response.json["items"][0]["professional_id"] == 1
        assert response.json["items"][0]["description"] == "Doente"
        assert response.json["items"][0]["diagnosis_type"] == "Definitivo"
        assert response.json["items"][0]["diagnosis_work"] == "Não"
        assert response.json["items"][0]["diagnosis_traffic_accident"] == "Sim"

    def test_get_medical_appointment_with_wrong_id(self, client):
        response = client.get("/appointment/100")
        assert response.status_code == 404
        assert response.json["message"] == "patient_not_found"

    # --------------------- POST ---------------------

    def test_register_medical_appointment_wrong_professional_id(
        self, client, base_medical_appointment
    ):
        base_medical_appointment["professional_id"] = 100
        response = client.post("/appointment", json=base_medical_appointment)

        assert response.status_code == 404
        assert response.json["message"] == "professional_not_found"

    def test_register_medical_appointment_wrong_patient_id(
        self, client, base_medical_appointment
    ):
        base_medical_appointment["patient_id"] = 100
        response = client.post("/appointment", json=base_medical_appointment)

        assert response.status_code == 404
        assert response.json["message"] == "patient_not_found"

    def test_register_medical_appointment_with_no_description(
        self, client, base_medical_appointment
    ):
        base_medical_appointment.pop("description", None)
        response = client.post("/appointment", json=base_medical_appointment)

        assert response.status_code == 400
        assert (
            response.json["errors"]["description"]
            == "'description' is a required property"
        )

    def test_register_medical_appointment_with_no_diagnosis_type(
        self, client, base_medical_appointment
    ):
        base_medical_appointment.pop("diagnosis_type", None)
        response = client.post("/appointment", json=base_medical_appointment)

        assert response.status_code == 400
        assert (
            response.json["errors"]["diagnosis_type"]
            == "'diagnosis_type' is a required property"
        )

    def test_register_medical_appointment_with_no_diagnosis_work(
        self, client, base_medical_appointment
    ):
        base_medical_appointment.pop("diagnosis_work", None)
        response = client.post("/appointment", json=base_medical_appointment)

        assert response.status_code == 400
        assert (
            response.json["errors"]["diagnosis_work"]
            == "'diagnosis_work' is a required property"
        )

    def test_register_medical_appointment_with_no_diagnosis_traffic_accident(
        self, client, base_medical_appointment
    ):
        base_medical_appointment.pop("diagnosis_traffic_accident", None)
        response = client.post("/appointment", json=base_medical_appointment)

        assert response.status_code == 400
        assert (
            response.json["errors"]["diagnosis_traffic_accident"]
            == "'diagnosis_traffic_accident' is a required property"
        )

    def test_register_medical_appointment_with_wrong_diagnosis_type(
        self, client, base_medical_appointment
    ):
        base_medical_appointment["diagnosis_type"] = "teste"
        response = client.post("/appointment", json=base_medical_appointment)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"

    def test_register_medical_appointment_with_wrong_diagnosis_work(
        self, client, base_medical_appointment
    ):
        base_medical_appointment["diagnosis_work"] = "teste"
        response = client.post("/appointment", json=base_medical_appointment)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"

    def test_register_medical_appointment_with_wrong_diagnosis_traffic_accident(
        self, client, base_medical_appointment
    ):
        base_medical_appointment["diagnosis_traffic_accident"] = "teste"
        response = client.post("/appointment", json=base_medical_appointment)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"

    def test_register_medical_appointment(self, client, base_medical_appointment):
        response = client.post("/appointment", json=base_medical_appointment)
        assert response.status_code == 201
        assert response.json["message"] == "patient_medical_appointment_created"
