import pytest

from app.main import db
from app.main.service import (
    add_patient_in_queue,
    create_default_queues,
    is_patient_in_queue,
)
from app.test.seeders import (
    create_base_seed_medical_prescription,
    create_base_seed_medicine,
    create_base_seed_patient,
    create_base_seed_procedure,
    create_base_seed_professional,
    create_base_seed_room,
)


@pytest.fixture(scope="module")
def seeded_database(client, database):
    """Seed database with medical prescription controller data"""

    create_default_queues()
    create_base_seed_professional(db)
    create_base_seed_patient(db)
    create_base_seed_medicine(db)
    create_base_seed_procedure(db)
    create_base_seed_room(db)

    add_patient_in_queue({"patient_id": 1, "queue_id": 2})

    return create_base_seed_medical_prescription(db)


@pytest.mark.usefixtures("seeded_database")
class TestMedicalPrescriptionController:

    # --------------------- GET ---------------------
    def test_get_medical_prescription(self, client):
        response = client.get("/medical_prescription")
        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 2
        assert response.json["total_pages"] == 1
        self._test_medical_prescription_response_data_item_one(
            data=response.json["items"][0]
        )
        self._test_medical_prescription_response_data_item_two(
            data=response.json["items"][1]
        )

    def test_get_medical_prescription_with_invalid_id(self, client):
        response = client.get("/medical_prescription/0")
        assert response.status_code == 404
        assert response.json["message"] == "medical_prescription_not_found"

    @pytest.mark.parametrize(
        "key, value, total_pages, total_items",
        [
            ("patient_id", 1, 1, 1),
            ("patient_id", 0, 0, 0),
            ("professional_id", 2, 1, 1),
            ("professional_id", 0, 0, 0),
        ],
    )
    def test_get_medical_prescription_by(
        self, client, key, value, total_pages, total_items
    ):
        response = client.get("/medical_prescription", query_string={key: value})
        assert response.status_code == 200
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == total_items
        assert response.json["total_pages"] == total_pages

        if value == 1:
            self._test_medical_prescription_response_data_item_one(
                response.json["items"][0]
            )
        elif value == 2:
            self._test_medical_prescription_response_data_item_two(
                response.json["items"][0]
            )

    # --------------------- POST ---------------------

    @pytest.mark.parametrize(
        "medical_prescription_type, queue_id",
        [("Observação", 3), ("Internação", 4)],
        ids=[
            "register_in_observation_room",
            "register_in_internation_room",
        ],
    )
    def test_register_medical_prescription_with_no_orientations(
        self, client, base_medical_prescription, medical_prescription_type, queue_id
    ):

        patient_id = base_medical_prescription["patient_id"]
        base_medical_prescription["type"] = medical_prescription_type

        base_medical_prescription.pop("orientations", None)
        response = client.post("/medical_prescription", json=base_medical_prescription)

        assert response.status_code == 201
        assert response.json["message"] == "medical_prescription_created"

        assert is_patient_in_queue(patient_id=patient_id, queue_id=queue_id) == True

    @pytest.mark.parametrize(
        "medical_prescription_type, queue_id",
        [("Observação", 3), ("Internação", 4)],
        ids=[
            "register_in_observation_room",
            "register_in_internation_room",
        ],
    )
    def test_register_medical_prescription_with_no_medicines(
        self, client, base_medical_prescription, medical_prescription_type, queue_id
    ):

        patient_id = base_medical_prescription["patient_id"]
        base_medical_prescription["type"] = medical_prescription_type

        base_medical_prescription.pop("medicines", None)
        response = client.post("/medical_prescription", json=base_medical_prescription)

        assert response.status_code == 201
        assert response.json["message"] == "medical_prescription_created"

        assert is_patient_in_queue(patient_id=patient_id, queue_id=queue_id) == True

    @pytest.mark.parametrize(
        "medical_prescription_type, queue_id",
        [("Observação", 3), ("Internação", 4)],
        ids=[
            "register_in_observation_room",
            "register_in_internation_room",
        ],
    )
    def test_register_medical_prescription_with_no_procedures(
        self, client, base_medical_prescription, medical_prescription_type, queue_id
    ):

        patient_id = base_medical_prescription["patient_id"]
        base_medical_prescription["type"] = medical_prescription_type

        base_medical_prescription.pop("procedures", None)
        response = client.post("/medical_prescription", json=base_medical_prescription)

        assert response.status_code == 201
        assert response.json["message"] == "medical_prescription_created"

        assert is_patient_in_queue(patient_id=patient_id, queue_id=queue_id) == True

    def test_register_medical_prescription_with_invalid_professional_id(
        self, client, base_medical_prescription
    ):
        base_medical_prescription["professional_id"] = 0
        response = client.post("/medical_prescription", json=base_medical_prescription)

        assert response.status_code == 404
        assert response.json["message"] == "professional_not_found"

    def test_register_medical_prescription_with_invalid_patient_id(
        self, client, base_medical_prescription
    ):
        base_medical_prescription["patient_id"] = 0
        response = client.post("/medical_prescription", json=base_medical_prescription)

        assert response.status_code == 404
        assert response.json["message"] == "patient_not_found"

    def test_register_medical_prescription_with_invalid_room_id(
        self, client, base_medical_prescription
    ):
        base_medical_prescription["room_id"] = 0
        response = client.post("/medical_prescription", json=base_medical_prescription)

        assert response.status_code == 404
        assert response.json["message"] == "room_not_found"

    def test_register_medical_prescription_with_invalid_medicine_id(
        self, client, base_medical_prescription
    ):
        base_medical_prescription["medicines"][0]["medicine_id"] = 0
        response = client.post("/medical_prescription", json=base_medical_prescription)

        assert response.status_code == 404
        assert response.json["message"] == "medical_prescription_medicine_not_found"

    def test_register_medical_prescription_with_invalid_procedure_id(
        self, client, base_medical_prescription
    ):
        base_medical_prescription["procedures"][0]["procedure_id"] = 0
        response = client.post("/medical_prescription", json=base_medical_prescription)

        assert response.status_code == 404
        assert response.json["message"] == "medical_prescription_procedure_not_found"

    @pytest.mark.parametrize(
        "key_popped",
        ["professional_id", "patient_id", "room_id", "type"],
        ids=[
            "register_without_professional_id",
            "register_without_patient_id",
            "register_without_room_id",
            "register_without_type",
        ],
    )
    def test_register_without_required_data(
        self, client, base_medical_prescription, key_popped
    ):

        patient_id = base_medical_prescription["patient_id"]

        base_medical_prescription.pop(key_popped, None)
        response = client.post("/medical_prescription", json=base_medical_prescription)

        assert response.status_code == 400
        assert key_popped in response.json["errors"].keys()

        assert is_patient_in_queue(patient_id=patient_id, queue_id=3) == False

    @pytest.mark.parametrize(
        "medical_prescription_type, queue_id",
        [("Observação", 3), ("Internação", 4)],
        ids=[
            "register_in_observation_room",
            "register_in_internation_room",
        ],
    )
    def test_register_medical_prescription(
        self, client, base_medical_prescription, medical_prescription_type, queue_id
    ):

        patient_id = base_medical_prescription["patient_id"]
        base_medical_prescription["type"] = medical_prescription_type

        response = client.post("/medical_prescription", json=base_medical_prescription)
        assert response.status_code == 201
        assert response.json["message"] == "medical_prescription_created"

        assert is_patient_in_queue(patient_id=patient_id, queue_id=queue_id) == True

    # --------------------- HELPER FUNCTIONS ---------------------

    def _test_medical_prescription_response_data_item_one(self, data: dict[str, any]):
        """Test medical prescription response data in get medical prescription item one"""

        assert data["professional_id"] == 1
        assert data["patient_id"] == 1
        assert data["room_id"] == 1
        assert len(data["orientations"]) == 1
        assert data["orientations"][0]["id"] == 1
        assert data["orientations"][0]["orientation"] == "Orientation One"
        assert data["orientations"][0]["execute_at"] == "25/08/1989 20:00:00"
        assert data["orientations"][0]["observations"] == "Orientation Observation One"
        assert len(data["medicines"]) == 1
        assert data["medicines"][0]["medicine"]["id"] == 1
        assert data["medicines"][0]["medicine"]["name"] == "Medicine One"
        assert data["medicines"][0]["execute_at"] == "25/08/1989 20:00:00"
        assert data["medicines"][0]["observations"] == "Medicine Observation One"
        assert len(data["procedures"]) == 1
        assert data["procedures"][0]["procedure"]["id"] == 1
        assert (
            data["procedures"][0]["procedure"]["description"]
            == "ATORVASTATINA 80 MG (POR COMPRIMIDO)"
        )
        assert data["procedures"][0]["execute_at"] == "25/08/1989 20:00:00"
        assert data["procedures"][0]["observations"] == "Procedure Observation One"

    def _test_medical_prescription_response_data_item_two(self, data: dict[str, any]):
        """Test medical prescription response data in get medical prescription item two"""

        assert data["professional_id"] == 2
        assert data["patient_id"] == 2
        assert data["room_id"] == 2
        assert len(data["orientations"]) == 1
        assert data["orientations"][0]["id"] == 2
        assert data["orientations"][0]["orientation"] == "Orientation Two"
        assert data["orientations"][0]["execute_at"] == "29/09/1989 19:00:00"
        assert data["orientations"][0]["observations"] == "Orientation Observation Two"
        assert len(data["medicines"]) == 1
        assert data["medicines"][0]["medicine"]["id"] == 2
        assert data["medicines"][0]["medicine"]["name"] == "Medicine Two"
        assert data["medicines"][0]["execute_at"] == "29/09/1989 19:00:00"
        assert data["medicines"][0]["observations"] == "Medicine Observation Two"
        assert len(data["procedures"]) == 1
        assert data["procedures"][0]["procedure"]["id"] == 2
        assert (
            data["procedures"][0]["procedure"]["description"]
            == "BEZAFIBRATO 200 MG (POR DRAGEA OU COMPRIMIDO)"
        )
        assert data["procedures"][0]["execute_at"] == "29/09/1989 19:00:00"
        assert data["procedures"][0]["observations"] == "Procedure Observation Two"
