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
def seeded_database(database):
    """Seed database with protocol data"""
    create_base_seed_action(db)
    create_base_seed_question(db)
    create_base_seed_protocol(db)
    create_base_seed_prescription(db)
    create_base_seed_diagnosis(db)


@pytest.mark.usefixtures("seeded_database")
class TestProtocolController:

    # --------------------- GET PROTOCOLS ---------------------
    def test_get_protocols(self, client):
        response = client.get("/protocol")

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 6
        assert response.json["total_pages"] == 1
        assert response.json["items"][0]["id"] == 1
        assert response.json["items"][0]["name"] == "PROTOCOL1"
        assert response.json["items"][0]["protocol_type"] == "Diagnóstico"
        assert response.json["items"][1]["id"] == 2
        assert response.json["items"][1]["name"] == "PROTOCOL2"
        assert response.json["items"][1]["protocol_type"] == "Prescrição"

    def test_get_protocols_setting_name(self, client):
        response = client.get("/protocol", query_string={"name": "PROTOCOL1"})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 1
        assert response.json["total_pages"] == 1
        assert response.json["items"][0]["id"] == 1
        assert response.json["items"][0]["name"] == "PROTOCOL1"
        assert response.json["items"][0]["protocol_type"] == "Diagnóstico"

    def test_get_protocols_setting_type_diagnosis(self, client):
        response = client.get(
            "/protocol", query_string={"protocol_type": "Diagnóstico"}
        )

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 3
        assert response.json["total_pages"] == 1
        assert response.json["items"][0]["id"] == 1
        assert response.json["items"][0]["name"] == "PROTOCOL1"
        assert response.json["items"][0]["protocol_type"] == "Diagnóstico"

    def test_get_protocols_setting_type_prescription(self, client):
        response = client.get("/protocol", query_string={"protocol_type": "Prescrição"})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 3
        assert response.json["total_pages"] == 1
        assert response.json["items"][0]["id"] == 2
        assert response.json["items"][0]["name"] == "PROTOCOL2"
        assert response.json["items"][0]["protocol_type"] == "Prescrição"

    def test_get_protocols_setting_wrong_type(self, client):
        response = client.get("/protocol", query_string={"protocol_type": "test"})
        assert response.status_code == 400
        assert response.json["message"] == "invalid_protocol_type"

    # --------------------- GET PROTOCOL BY ID ---------------------

    def test_get_protocol_by_id(self, client):
        response = client.get("/protocol/1")
        assert response.status_code == 200
        assert response.json["name"] == "PROTOCOL1"

    def test_get_protocol_with_wrong_id(self, client):
        response = client.get("/protocol/0")
        assert response.status_code == 404
        assert response.json["message"] == "protocol_not_found"

    # --------------------- UPDATE ---------------------

    def test_update_protocol_with_same_name_and_type(self, client):
        response = client.put(
            "/protocol/1",
            json={"name": "PROTOCOL1", "protocol_type": "Diagnóstico"},
        )
        assert response.status_code == 409
        assert response.json["message"] == "protocol_already_exist"

    def test_update_protocol_only_with_name(self, client):
        response = client.put("/protocol/1", json={"name": "questão23"})

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"

    def test_update_protocol_only_with_type(self, client):
        response = client.put("/protocol/1", json={"protocol_type": "Prescrição"})

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"

    def test_update_protocol_with_no_argument(self, client):
        response = client.post("/protocol", json={})

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"

    def test_update_protocol_with_invalid_name_format(self, client):
        response = client.put(
            "/protocol/1", json={"name": 1, "protocol_type": "Prescrição"}
        )

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"

    @pytest.mark.parametrize(
        "invalid_enum_and_type",
        ["teste", 1],
    )
    def test_update_protocol_with_invalid_enum_and_type_format(
        self, client, invalid_enum_and_type
    ):
        response = client.put(
            "/protocol/1",
            json={"name": "nada", "protocol_type": invalid_enum_and_type},
        )

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"

    def test_update_protocol_with_invalid_id(self, client):
        response = client.put(
            "/protocol/0",
            json={"name": "questão23", "protocol_type": "Diagnóstico"},
        )

        assert response.status_code == 404
        assert response.json["message"] == "protocol_not_found"

    def test_update_protocol_with_empty_name(self, client):
        response = client.put(
            "/protocol/1", json={"name": "", "protocol_type": "Prescrição"}
        )

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert "name" in response.json["errors"].keys()

    def test_update_protocol_changing_name(self, client):
        response = client.put(
            "/protocol/1",
            json={"name": "questão23", "protocol_type": "Diagnóstico"},
        )

        assert response.status_code == 200
        assert response.json["message"] == "protocol_updated"

    def test_update_protocol_associated_with_diagnosis(self, client):
        response = client.put(
            "/protocol/1",
            json={"name": "protocol put", "protocol_type": "Prescrição"},
        )

        assert response.status_code == 409
        assert response.json["message"] == "protocol_is_associated_with_diagnosis"

    def test_update_protocol_associated_with_prescription(self, client):
        response = client.put(
            "/protocol/2",
            json={"name": "protocol put", "protocol_type": "Diagnóstico"},
        )

        assert response.json["message"] == "protocol_is_associated_with_prescription"

        assert response.status_code == 409

    def test_update_protocol_changing_type(self, client):
        response = client.put(
            "/protocol/3",
            json={
                "name": "protocol changing type",
                "protocol_type": "Prescrição",
            },
        )

        assert response.status_code == 200
        assert response.json["message"] == "protocol_updated"

    def test_update_protocol_changing_name_and_type(self, client):
        response = client.put(
            "/protocol/5",
            json={
                "name": "protocol changing_name_and_type",
                "protocol_type": "Diagnóstico",
            },
        )

        assert response.status_code == 200
        assert response.json["message"] == "protocol_updated"

    # --------------------- POST ---------------------

    def test_register_protocol_with_no_argument(self, client):
        response = client.post("/protocol", json={})

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"

    def test_register_protocol_with_no_name(self, client):
        response = client.post("/protocol", json={"protocol_type": "Diagnóstico"})
        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"

    def test_register_protocol_with_no_type(self, client):
        response = client.post("/protocol", json={"name": "descrição massa"})
        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"

    @pytest.mark.parametrize(
        "name,protocol_type",
        [("descrição", 1), (1, "Diagnóstico"), ("Test", "blabla")],
    )
    def test_register_protocol_with_invalid_type_name_and_enum_format(
        self, client, name, protocol_type
    ):
        response = client.post(
            "/protocol",
            json={"name": name, "protocol_type": protocol_type},
        )
        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"

    def test_register_protocol_with_empty_name(self, client):
        response = client.post(
            "/protocol", json={"name": "", "protocol_type": "Prescrição"}
        )

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert "name" in response.json["errors"].keys()

    def test_register_protocol(self, client, base_protocol):
        response = client.post("/protocol", json=base_protocol)

        assert response.status_code == 201
        assert response.json["message"] == "protocol_created"

    # --------------------- DELETE ---------------------

    def test_delete_protocol_associated_with_diagnosis(self, client):
        response = client.delete("/protocol/1")

        assert response.status_code == 409
        assert response.json["message"] == "protocol_is_associated_with_diagnosis"

    def test_delete_protocol_associated_with_prescription(self, client):
        response = client.delete("/protocol/2")

        assert response.status_code == 409
        assert response.json["message"] == "protocol_is_associated_with_prescription"

    def test_delete_protocol_with_invalid_id(self, client):
        response = client.delete("/protocol/0")

        assert response.status_code == 404
        assert response.json["message"] == "protocol_not_found"

    def test_delete_protocol_no_associated(self, client):
        response = client.delete("/protocol/3")

        assert response.status_code == 200
        assert response.json["message"] == "protocol_deleted"
