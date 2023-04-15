import pytest
from sqlalchemy.orm import joinedload

from app.main import db
from app.main.model import QueueManager
from app.main.service import create_default_queues
from app.test.seeders import (
    create_base_seed_patient,
    create_base_seed_professional,
    create_base_seed_queue_manager,
    create_base_seed_risk_classification,
)


@pytest.fixture(scope="module")
def seeded_database(client, database):
    """Seed database with risk classification controller data"""

    create_default_queues()
    create_base_seed_professional(db)
    create_base_seed_patient(db)
    create_base_seed_queue_manager(db)
    return create_base_seed_risk_classification(db)


@pytest.mark.usefixtures("seeded_database")
class TestRiskClassificationController:

    # --------------------- GET BY PATIENT ---------------------
    def test_get_risk_classification_history_by_patient(self, client):
        response = client.get("/risk/patient/1")

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 1

        self._test_risk_classification_data(item=response.json["items"][0])

    def test_get_risk_classification_history_by_non_registered_patient(self, client):
        response = client.get("/risk/patient/123")

        assert response.status_code == 404
        assert response.json["message"] == "patient_not_found"

    # --------------------- GET BY ID ---------------------
    def test_get_risk_classification_by_id(self, client):
        response = client.get("/risk/1")

        assert response.status_code == 200

        self._test_risk_classification_data(item=response.json)

    def test_get_risk_classification_by_non_registered_id(self, client):
        response = client.get("/risk/0")

        assert response.status_code == 404
        assert response.json["message"] == "risk_classification_not_found"

    # --------------------- PUT ---------------------
    def test_update_risk_classification_by_non_registered_id(
        self, client, base_risk_classification
    ):
        response = client.put("/risk/0", json=base_risk_classification)

        assert response.status_code == 404
        assert response.json["message"] == "risk_classification_not_found"

    @pytest.mark.parametrize(
        "key_popped",
        [
            "sys_blood_pressure",
            "dia_blood_pressure",
            "temperature",
            "heart_pulse",
            "risk_classification",
            "weight",
        ],
        ids=[
            "update_without_sys_blood_pressure",
            "update_without_dia_blood_pressure",
            "update_without_temperature",
            "update_without_heart_pulse",
            "update_without_risk_classification",
            "update_without_weight",
        ],
    )
    def test_update_risk_without_required_data(
        self, client, base_risk_classification, key_popped
    ):
        base_risk_classification.pop(key_popped, None)
        response = client.put("/risk/1", json=base_risk_classification)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert key_popped in response.json["errors"].keys()

    @pytest.mark.parametrize(
        "key",
        [
            "risk_classification",
            "eye_opening",
            "verbal_response",
            "eye_opening",
            "motor_response",
        ],
        ids=[
            "register_with_wrong_risk_classification",
            "register_with_wrong_eye_opening",
            "register_with_wrong_verbal_response",
            "register_with_wrong_eye_opening",
            "register_with_wrong_motor_response",
        ],
    )
    def test_update_risk_with_wrong_enum_data(
        self, client, base_risk_classification, key
    ):
        base_risk_classification[key] = "teste"
        response = client.put("/risk/1", json=base_risk_classification)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert key in response.json["errors"].keys()

    def test_update_risk_classification(self, client, base_risk_classification):
        response = client.put("/risk/1", json=base_risk_classification)

        assert response.status_code == 200
        assert response.json["message"] == "risk_classification_updated"

    # --------------------- POST ---------------------

    def test_register_risk_of_patient_already_with_risk_classification(
        self, client, base_risk_classification
    ):
        base_risk_classification["patient_id"] = 3
        response = client.post("/risk", json=base_risk_classification)

        assert response.status_code == 409
        assert response.json["message"] == "patient_risk_classification_already_exists"

    @pytest.mark.parametrize(
        "key_popped",
        [
            "patient_id",
            "professional_id",
            "sys_blood_pressure",
            "dia_blood_pressure",
            "temperature",
            "heart_pulse",
            "risk_classification",
            "weight",
        ],
        ids=[
            "register_without_patient_id",
            "register_without_professional_id",
            "register_without_sys_blood_pressure",
            "register_without_dia_blood_pressure",
            "register_without_temperature",
            "register_without_heart_pulse",
            "register_without_risk_classification",
            "register_without_weight",
        ],
    )
    def test_register_risk_without_required_data(
        self, client, base_risk_classification, key_popped
    ):
        base_risk_classification.pop(key_popped, None)
        response = client.post("/risk", json=base_risk_classification)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert key_popped in response.json["errors"].keys()

    @pytest.mark.parametrize(
        "key",
        [
            "risk_classification",
            "eye_opening",
            "verbal_response",
            "eye_opening",
            "motor_response",
        ],
        ids=[
            "register_with_wrong_risk_classification",
            "register_with_wrong_eye_opening",
            "register_with_wrong_verbal_response",
            "register_with_wrong_eye_opening",
            "register_with_wrong_motor_response",
        ],
    )
    def test_register_risk_with_wrong_enum_data(
        self, client, base_risk_classification, key
    ):
        base_risk_classification[key] = "teste"
        response = client.post("/risk", json=base_risk_classification)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert key in response.json["errors"].keys()

    def test_register_risk_with_non_registered_patient(
        self, client, base_risk_classification
    ):
        base_risk_classification["patient_id"] = 0
        response = client.post("/risk", json=base_risk_classification)

        assert response.status_code == 404
        assert response.json["message"] == "patient_not_found"

    def test_register_risk_with_non_registered_professional(
        self, client, base_risk_classification
    ):
        base_risk_classification["patient_id"] = 9
        base_risk_classification["professional_id"] = 0
        response = client.post("/risk", json=base_risk_classification)

        assert response.json["message"] == "professional_not_found"

    def test_register_risk_classification(self, client, base_risk_classification):
        response = client.post("/risk", json=base_risk_classification)

        assert response.json["message"] == "patient_risk_classification_created"
        assert response.status_code == 201

        queue_manager = (
            QueueManager.query.options(joinedload("risk_classification"))
            .filter(
                QueueManager.patient_id == base_risk_classification["patient_id"],
                QueueManager.hospital_exit.is_(None),
            )
            .first()
        )

        assert queue_manager is not None
        assert queue_manager.risk_classification is not None
        assert queue_manager.queue_id == 2

    def test_register_risk_classification_emergency(self, client):
        response = client.post(
            "/risk",
            json={
                "patient_id": 9,
                "professional_id": 1,
                "risk_classification": "Emergência",
            },
        )
        assert response.status_code == 201
        assert response.json["message"] == "patient_risk_classification_created"

    # --------------------- Helper Functions ---------------------
    def _test_risk_classification_data(self, item: dict[str, any]) -> None:

        assert item["weight"] == 67.48
        assert item["height"] == 1.69
        assert item["sys_blood_pressure"] == 120
        assert item["dia_blood_pressure"] == 80
        assert item["temperature"] == 37.8
        assert item["heart_pulse"] == 120
        assert item["respiratory_frequence"] == 15
        assert item["diabetic"] == False
        assert item["capillary_blood_glucose"] == 80
        assert item["eye_opening"] == "À Dor"
        assert item["verbal_response"] == "Palavras incompreensíveis"
        assert item["motor_response"] == "Flexão Anormal"
        assert item["pupillary_reactivity"] == "Reação bilateral ao estímulo"
        assert item["fasting"] == True
        assert item["professional_avaliation"] == "Professional Avaliation"
        assert item["risk_classification"] == "Urgente"
