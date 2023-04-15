import pytest

from app.main import db
from app.test.seeders import (
    create_base_seed_action,
    create_base_seed_prescription,
    create_base_seed_protocol,
)


@pytest.fixture(scope="module")
def seeded_database(client, database):
    """Seed database with prescription data"""

    create_base_seed_protocol(db)
    create_base_seed_action(db)
    create_base_seed_prescription(db)


@pytest.mark.usefixtures("seeded_database")
class TestPrescriptionController:

    # --------------------- GET PRESCRIPTIONS ---------------------

    def test_get_prescriptions(self, client):
        response = client.get("/prescription")

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 2
        assert response.json["total_pages"] == 1

        self._test_prescription_response_data(data=response.json["items"][0])

    def test_get_prescriptions_by_page(self, client):
        response = client.get("/prescription", query_string={"page": 2})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert len(response.json["items"]) == 0
        assert response.json["current_page"] == 2

    @pytest.mark.parametrize(
        "protocol", ["PROTOCOL2", "2"], ids=["complete_protocol", "incomplete_protocol"]
    )
    def test_get_prescription_by_protocol(self, client, protocol):
        response = client.get("/prescription", query_string={"protocol": protocol})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["total_items"] == 1
        self._test_prescription_response_data(data=response.json["items"][0])

    # --------------------- GET PRESCRIPTION  BY ID ---------------------

    def test_get_prescription_by_id(self, client):
        response = client.get("/prescription/1")

        assert response.status_code == 200
        self._test_prescription_response_data(data=response.json)

    def test_get_prescription_by_invalid_id(self, client):
        response = client.get("/prescription/0")

        assert response.status_code == 404
        assert response.json["message"] == "prescription_not_found"

    # --------------------- UPDATE PRESCRIPTION ---------------------

    def test_update_prescription_with_invalid_protocol_id(
        self, client, base_prescription
    ):
        base_prescription["protocol_id"] = 0

        response = client.put("/prescription/1", json=base_prescription)

        assert response.status_code == 404
        assert response.json["message"] == "protocol_not_found"

    def test_update_prescription_with_invalid_action_id(
        self, client, base_prescription
    ):
        base_prescription["actions_ids"][0] = 10

        response = client.put("/prescription/1", json=base_prescription)

        assert response.status_code == 404
        assert response.json["message"] == "action_not_found"

    def test_update_prescription_with_invalid_prescription_id(
        self, client, base_prescription
    ):
        response = client.put("/prescription/0", json=base_prescription)

        assert response.status_code == 404
        assert response.json["message"] == "prescription_not_found"

    def test_update_prescription_with_invalid_protocol_type(
        self, client, base_prescription
    ):
        base_prescription["protocol_id"] = 1

        response = client.put("/prescription/1", json=base_prescription)

        assert response.status_code == 409
        assert response.json["message"] == "protocol_is_not_prescription_type"

    def test_update_prescription_with_protocol_already_associated(
        self, client, base_prescription
    ):
        base_prescription["protocol_id"] = 4

        response = client.put("/prescription/1", json=base_prescription)

        assert response.status_code == 409
        assert (
            response.json["message"] == "protocol_already_associated_with_prescription"
        )

    @pytest.mark.parametrize(
        "key_popped",
        ["protocol_id", "actions_ids"],
        ids=["without_protocol_id", "without_action_id_list"],
    )
    def test_update_prescription_without_required_data(
        self, client, base_prescription, key_popped
    ):
        base_prescription.pop(key_popped, None)

        response = client.post("/prescription", json=base_prescription)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert key_popped in response.json["errors"].keys()

    def test_update_prescription(self, client, base_prescription):
        response = client.put("/prescription/1", json=base_prescription)

        assert response.status_code == 200
        assert response.json["message"] == "prescription_updated"

    # --------------------- CREATE PRESCRIPTION ---------------------

    @pytest.mark.parametrize(
        "key,new_value,expected_message",
        [
            ("protocol_id", 0, "protocol_not_found"),
            ("actions_ids", [0], "action_not_found"),
        ],
        ids=["invalid_protocol_id", "invalid_action_id"],
    )
    def test_create_prescription_with_invalid_data_id(
        self, client, base_prescription, key, new_value, expected_message
    ):
        base_prescription["protocol_id"] = 2
        base_prescription[key] = new_value

        response = client.post("/prescription", json=base_prescription)

        assert response.status_code == 404
        assert response.json["message"] == expected_message

    def test_create_prescription_with_invalid_protocol_type(
        self, client, base_prescription
    ):
        base_prescription["protocol_id"] = 1

        response = client.post("/prescription", json=base_prescription)

        assert response.status_code == 409
        assert response.json["message"] == "protocol_is_not_prescription_type"

    def test_create_prescription_with_protocol_already_associated(
        self, client, base_prescription
    ):

        response = client.post("/prescription", json=base_prescription)

        assert response.status_code == 409
        assert (
            response.json["message"] == "protocol_already_associated_with_prescription"
        )

    @pytest.mark.parametrize(
        "key_popped",
        ["protocol_id", "actions_ids"],
        ids=["without_protocol_id", "without_action_id_list"],
    )
    def test_create_prescription_without_required_data(
        self, client, base_prescription, key_popped
    ):
        base_prescription.pop(key_popped, None)

        response = client.post("/prescription", json=base_prescription)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert key_popped in response.json["errors"].keys()

    def test_create_prescription(self, client, base_prescription):
        base_prescription["protocol_id"] = 2
        base_prescription["actions_id"] = [2]
        response = client.post("/prescription", json=base_prescription)

        assert response.status_code == 201
        assert response.json["message"] == "prescription_created"

    # --------------------- DELETE PRESCRIPTION ---------------------

    def test_delete_prescription_with_non_registered_id(self, client):
        response = client.delete("/prescription/0")

        assert response.status_code == 404
        assert response.json["message"] == "prescription_not_found"

    def test_delete_prescription(self, client):
        response = client.delete("/prescription/1")

        assert response.status_code == 200
        assert response.json["message"] == "prescription_deleted"

    # --------------------- Helper functions ---------------------

    def _test_prescription_response_data(self, data: dict[str, any]):
        """Test prescription response data in get prescription"""

        assert data["protocol"] == {
            "id": 2,
            "name": "PROTOCOL2",
            "protocol_type": "Prescrição",
        }
        assert len(data["actions"]) == 1
        assert data["actions"][0] == {"id": 1, "name": "AÇÃO TESTE 1"}
