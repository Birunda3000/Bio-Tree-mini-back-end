import pytest

from app.main import db
from app.test.seeders import (
    create_base_seed_action,
    create_base_seed_diagnosis,
    create_base_seed_prescription,
    create_base_seed_protocol,
    create_base_seed_question,
)


@pytest.fixture(scope="module")
def seeded_database(client, database):
    """Seed database with diagnosis data"""
    create_base_seed_action(db)
    create_base_seed_question(db)
    create_base_seed_protocol(db)
    create_base_seed_prescription(db)
    create_base_seed_diagnosis(db)


@pytest.mark.usefixtures("seeded_database")
class TestDiagnosisController:

    # --------------------- GET DIAGNOSIS ---------------------

    def test_get_diagnosis(self, client):
        response = client.get("/diagnosis")

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 2
        assert response.json["total_pages"] == 1

        self._test_diagnosis_response_data(data=response.json["items"][0])

    def test_get_diagnosis_by_page(self, client):
        response = client.get("/diagnosis", query_string={"page": 2})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert len(response.json["items"]) == 0
        assert response.json["current_page"] == 2

    @pytest.mark.parametrize(
        "protocol", ["PROTOCOL1", "1"], ids=["complete_protocol", "incomplete_protocol"]
    )
    def test_get_diagnosis_by_protocol(self, client, protocol):
        response = client.get("/diagnosis", query_string={"protocol": protocol})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["total_items"] == 1
        self._test_diagnosis_response_data(data=response.json["items"][0])

    # --------------------- UPDATE DIAGNOSIS ---------------------

    def test_update_diagnosis_with_invalid_protocol_id(self, client, base_diagnosis):
        base_diagnosis["protocol_id"] = 0

        response = client.put("/diagnosis/1", json=base_diagnosis)

        assert response.status_code == 404
        assert response.json["message"] == "protocol_not_found"

    def test_update_diagnosis_with_invalid_question_id(self, client, base_diagnosis):
        base_diagnosis["questions_ids"][0] = 10

        response = client.put("/diagnosis/1", json=base_diagnosis)

        assert response.status_code == 404
        assert response.json["message"] == "question_not_found"

    def test_update_diagnosis_with_invalid_prescription_id(
        self, client, base_diagnosis
    ):
        response = client.put("/diagnosis/0", json=base_diagnosis)

        assert response.status_code == 404
        assert response.json["message"] == "diagnosis_not_found"

    def test_update_diagnosis_with_invalid_protocol_type(self, client, base_diagnosis):
        base_diagnosis["protocol_id"] = 2

        response = client.put("/diagnosis/1", json=base_diagnosis)

        assert response.status_code == 409
        assert response.json["message"] == "protocol_is_not_diagnosis_type"

    def test_update_diagnosis_with_protocol_already_associated(
        self, client, base_diagnosis
    ):
        base_diagnosis["protocol_id"] = 6

        response = client.put("/diagnosis/1", json=base_diagnosis)

        assert response.status_code == 409
        assert response.json["message"] == "protocol_already_associated_with_diagnosis"

    def test_update_diagnosis(self, client, base_diagnosis):
        base_diagnosis["protocol_id"] = 1

        response = client.put("/diagnosis/1", json=base_diagnosis)

        assert response.status_code == 200
        assert response.json["message"] == "diagnosis_updated"

    # --------------------- CREATE DIAGNOSIS ---------------------

    @pytest.mark.parametrize(
        "key,new_value,expected_message",
        [
            ("protocol_id", 0, "protocol_not_found"),
            ("questions_ids", [0], "question_not_found"),
        ],
        ids=["invalid_protocol_id", "invalid_diagnosis_id"],
    )
    def test_create_diagnosis_with_invalid_data_id(
        self, client, base_diagnosis, key, new_value, expected_message
    ):
        base_diagnosis[key] = new_value

        response = client.post("/diagnosis", json=base_diagnosis)

        assert response.status_code == 404
        assert response.json["message"] == expected_message

    def test_create_diagnosis_with_invalid_protocol_type(self, client, base_diagnosis):
        base_diagnosis["protocol_id"] = 2

        response = client.post("/diagnosis", json=base_diagnosis)

        assert response.status_code == 409
        assert response.json["message"] == "protocol_is_not_diagnosis_type"

    def test_create_diagnosis_with_protocol_already_associated(
        self, client, base_diagnosis
    ):
        base_diagnosis["protocol_id"] = 1
        response = client.post("/diagnosis", json=base_diagnosis)

        assert response.status_code == 409
        assert response.json["message"] == "protocol_already_associated_with_diagnosis"

    @pytest.mark.parametrize(
        "key_popped",
        ["protocol_id", "questions_ids"],
        ids=["without_protocol_id", "without_question_id_list"],
    )
    def test_create_diagnosis_without_required_data(
        self, client, base_diagnosis, key_popped
    ):
        base_diagnosis.pop(key_popped, None)

        response = client.post("/diagnosis", json=base_diagnosis)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert key_popped in response.json["errors"].keys()

    def test_create_diagnosis(self, client, base_diagnosis):
        base_diagnosis["questions_ids"] = [1]

        response = client.post("/diagnosis", json=base_diagnosis)

        assert response.status_code == 201
        assert response.json["message"] == "diagnosis_created"

    # --------------------- DELETE DIAGNOSIS ---------------------

    def test_delete_diagnosis_with_non_registered_id(self, client):
        response = client.delete("/diagnosis/0")

        assert response.status_code == 404
        assert response.json["message"] == "diagnosis_not_found"

    def test_delete_diagnosis(self, client):
        response = client.delete("/diagnosis/1")

        assert response.status_code == 200
        assert response.json["message"] == "diagnosis_deleted"

    # --------------------- HELPER FUNCTIONS ---------------------

    def _test_diagnosis_response_data(self, data: dict[str, any]):
        """Test diagnosis response data in get diagnosis"""

        assert data["protocol"] == {
            "id": 1,
            "name": "PROTOCOL1",
            "protocol_type": "Diagnóstico",
        }
        assert len(data["questions"]) == 1
        assert data["questions"][0] == {"id": 1, "name": "PERGUNTA1"}
