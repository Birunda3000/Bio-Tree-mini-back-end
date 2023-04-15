import pytest

from app.main import db
from app.main.service import get_physical_installation_type
from app.test.seeders import create_base_seed_physical_installation_type


@pytest.fixture(scope="module")
def seeded_database(client, database):
    """Seed database with physical installation type data"""
    return create_base_seed_physical_installation_type(db)


@pytest.mark.usefixtures("seeded_database")
class TestPhysicalInstallationTypeController:

    # --------------------- GET ---------------------
    def test_get_physical_installation_types(self, client):
        response = client.get("/physical_installation/type")

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 2
        assert response.json["total_pages"] == 1
        assert response.json["items"][0]["id"] == 1
        assert response.json["items"][0]["name"] == "TIPO DE INSTALAÇÃO FÍSICA TESTE 1"
        assert response.json["items"][1]["id"] == 2
        assert response.json["items"][1]["name"] == "TIPO DE INSTALAÇÃO FÍSICA TESTE 2"

    def test_get_physical_installation_types_by_page(self, client):
        response = client.get("/physical_installation/type", query_string={"page": 2})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert len(response.json["items"]) == 0
        assert response.json["current_page"] == 2

    def test_get_physical_installation_types_by_name(self, client):
        response = client.get(
            "/physical_installation/type", query_string={"name": "TESTE 1"}
        )

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 1
        assert response.json["total_pages"] == 1
        assert response.json["items"][0]["id"] == 1
        assert response.json["items"][0]["name"] == "TIPO DE INSTALAÇÃO FÍSICA TESTE 1"

    # --------------------- GET BY ID ---------------------

    def test_get_physical_installation_type(self, client):
        response = client.get("/physical_installation/type/1")

        assert response.status_code == 200
        assert response.json["id"] == 1
        assert response.json["name"] == "TIPO DE INSTALAÇÃO FÍSICA TESTE 1"

    def test_get_physical_installation_type_with_invalid_id(self, client):
        response = client.get("/physical_installation/type/0")

        assert response.json["message"] == "physical_installation_type_not_found"
        assert response.status_code == 404

    # --------------------- PUT ---------------------

    def test_update_physical_installation_type_with_invalid_id(
        self, client, base_physical_installation_type
    ):
        response = client.put(
            "/physical_installation/type/0", json=base_physical_installation_type
        )

        assert response.json["message"] == "physical_installation_type_not_found"
        assert response.status_code == 404

    def test_update_physical_installation_type_without_required_data(
        self, client, base_physical_installation_type
    ):
        base_physical_installation_type.pop("name", None)
        response = client.put(
            "/physical_installation/type/1", json=base_physical_installation_type
        )

        assert response.json["message"] == "Input payload validation failed"
        assert response.status_code == 400

    def test_update_physical_installation_type_with_registered_name(
        self, client, base_physical_installation_type
    ):
        base_physical_installation_type["name"] = "TIPO DE INSTALAÇÃO FÍSICA TESTE 2"
        response = client.put(
            "/physical_installation/type/1", json=base_physical_installation_type
        )

        assert response.json["message"] == "name_in_use"
        assert response.status_code == 409

    def test_update_physical_installation_type_with_empty_name(
        self, client, base_physical_installation_type
    ):
        base_physical_installation_type["name"] = ""
        response = client.put(
            "/physical_installation/type/1", json=base_physical_installation_type
        )

        assert response.json["message"] == "Input payload validation failed"
        assert response.status_code == 400
        assert "name" in response.json["errors"].keys()

    def test_update_physical_installation_type(
        self, client, base_physical_installation_type
    ):
        response = client.put(
            "/physical_installation/type/1", json=base_physical_installation_type
        )

        physical_installation_type = get_physical_installation_type(
            physical_installation_type_id=1
        )

        assert response.json["message"] == "physical_installation_type_updated"
        assert response.status_code == 200
        assert physical_installation_type.name == "TIPO DE INSTALAÇÃO FÍSICA TESTE 3"

    # --------------------- POST --------------------

    def test_create_physical_installation_type_with_registered_name(
        self, client, base_physical_installation_type
    ):
        response = client.post(
            "/physical_installation/type", json=base_physical_installation_type
        )

        assert response.json["message"] == "name_in_use"
        assert response.status_code == 409

    def test_create_physical_installation_type_without_required_data(
        self, client, base_physical_installation_type
    ):
        base_physical_installation_type.pop("name", None)
        response = client.post(
            "/physical_installation/type", json=base_physical_installation_type
        )

        assert response.json["message"] == "Input payload validation failed"
        assert response.status_code == 400

    def test_create_physical_installation_type_with_empty_name(
        self, client, base_physical_installation_type
    ):
        base_physical_installation_type["name"] = ""
        response = client.post(
            "/physical_installation/type", json=base_physical_installation_type
        )

        assert response.json["message"] == "Input payload validation failed"
        assert response.status_code == 400
        assert "name" in response.json["errors"].keys()

    def test_create_physical_installation_type(
        self, client, base_physical_installation_type
    ):
        base_physical_installation_type["name"] = "TIPO DE INSTALAÇÃO FÍSICA TESTE 1"
        response = client.post(
            "/physical_installation/type", json=base_physical_installation_type
        )

        assert response.json["message"] == "physical_installation_type_created"
        assert response.status_code == 201

    # --------------------- DELETE ---------------------
    def test_delete_physical_installation_type_with_invalid_id(self, client):
        response = client.delete("/physical_installation/type/0")

        assert response.json["message"] == "physical_installation_type_not_found"
        assert response.status_code == 404

    def test_delete_physical_installation_type(self, client):

        response = client.delete("/physical_installation/type/1")

        assert response.json["message"] == "physical_installation_type_deleted"
        assert response.status_code == 200
