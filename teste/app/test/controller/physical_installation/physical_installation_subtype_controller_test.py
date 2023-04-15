import pytest

from app.main import db
from app.main.service import get_physical_installation_subtype
from app.test.seeders import create_base_seed_physical_installation_subtype


@pytest.fixture(scope="module")
def seeded_database(client, database):
    """Seed database with physical installation subtype data"""
    return create_base_seed_physical_installation_subtype(db)


@pytest.mark.usefixtures("seeded_database")
class TestPhysicalInstallationSubtypeController:

    # --------------------- GET ---------------------
    def test_get_physical_installation_subtypes(self, client):
        response = client.get("/physical_installation/subtype")

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 2
        assert response.json["total_pages"] == 1
        assert response.json["items"][0]["id"] == 1
        assert (
            response.json["items"][0]["name"] == "SUBTIPO DE INSTALAÇÃO FÍSICA TESTE 1"
        )
        assert response.json["items"][1]["id"] == 2
        assert (
            response.json["items"][1]["name"] == "SUBTIPO DE INSTALAÇÃO FÍSICA TESTE 2"
        )

    def test_get_physical_installation_subtypes_by_page(self, client):
        response = client.get(
            "/physical_installation/subtype", query_string={"page": 2}
        )

        assert response.status_code == 200
        assert len(response.json) == 4
        assert len(response.json["items"]) == 0
        assert response.json["current_page"] == 2

    def test_get_physical_installation_subtypes_by_name(self, client):
        response = client.get(
            "/physical_installation/subtype", query_string={"name": "TESTE 1"}
        )

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 1
        assert response.json["total_pages"] == 1
        assert response.json["items"][0]["id"] == 1
        assert (
            response.json["items"][0]["name"] == "SUBTIPO DE INSTALAÇÃO FÍSICA TESTE 1"
        )

    # --------------------- GET BY ID ---------------------

    def test_get_physical_installation_subtype(self, client):
        response = client.get("/physical_installation/subtype/1")

        assert response.status_code == 200
        assert response.json["id"] == 1
        assert response.json["name"] == "SUBTIPO DE INSTALAÇÃO FÍSICA TESTE 1"

    def test_get_physical_installation_subtype_with_invalid_id(self, client):
        response = client.get("/physical_installation/subtype/0")

        assert response.json["message"] == "physical_installation_subtype_not_found"
        assert response.status_code == 404

    # --------------------- PUT ---------------------

    def test_update_physical_installation_subtype_with_invalid_id(
        self, client, base_physical_installation_subtype
    ):
        response = client.put(
            "/physical_installation/subtype/0", json=base_physical_installation_subtype
        )

        assert response.json["message"] == "physical_installation_subtype_not_found"
        assert response.status_code == 404

    def test_update_physical_installation_subtype_without_required_data(
        self, client, base_physical_installation_subtype
    ):
        base_physical_installation_subtype.pop("name", None)
        response = client.put(
            "/physical_installation/subtype/1", json=base_physical_installation_subtype
        )

        assert response.json["message"] == "Input payload validation failed"
        assert response.status_code == 400

    def test_update_physical_installation_subtype_with_registered_name(
        self, client, base_physical_installation_subtype
    ):
        base_physical_installation_subtype[
            "name"
        ] = "SUBTIPO DE INSTALAÇÃO FÍSICA TESTE 2"
        response = client.put(
            "/physical_installation/subtype/1", json=base_physical_installation_subtype
        )

        assert response.json["message"] == "name_in_use"
        assert response.status_code == 409

    def test_update_physical_installation_subtype_with_empty_name(
        self, client, base_physical_installation_subtype
    ):
        base_physical_installation_subtype["name"] = ""
        response = client.put(
            "/physical_installation/subtype/1", json=base_physical_installation_subtype
        )

        assert response.json["message"] == "Input payload validation failed"
        assert response.status_code == 400
        assert "name" in response.json["errors"].keys()

    def test_update_physical_installation_subtype(
        self, client, base_physical_installation_subtype
    ):
        response = client.put(
            "/physical_installation/subtype/1", json=base_physical_installation_subtype
        )

        physical_installation_subtype = get_physical_installation_subtype(
            physical_installation_subtype_id=1
        )

        assert response.json["message"] == "physical_installation_subtype_updated"
        assert response.status_code == 200
        assert (
            physical_installation_subtype.name == "SUBTIPO DE INSTALAÇÃO FÍSICA TESTE 3"
        )

    # --------------------- POST --------------------

    def test_create_physical_installation_subtype_without_required_data(
        self, client, base_physical_installation_subtype
    ):
        base_physical_installation_subtype.pop("name", None)
        response = client.post(
            "/physical_installation/subtype", json=base_physical_installation_subtype
        )

        assert response.json["message"] == "Input payload validation failed"
        assert response.status_code == 400

    def test_create_physical_installation_subtype_with_registered_name(
        self, client, base_physical_installation_subtype
    ):
        response = client.post(
            "/physical_installation/subtype", json=base_physical_installation_subtype
        )

        assert response.json["message"] == "name_in_use"
        assert response.status_code == 409

    def test_create_physical_installation_subtype_with_empty_name(
        self, client, base_physical_installation_subtype
    ):
        base_physical_installation_subtype["name"] = ""
        response = client.post(
            "/physical_installation/subtype", json=base_physical_installation_subtype
        )

        assert response.json["message"] == "Input payload validation failed"
        assert response.status_code == 400
        assert "name" in response.json["errors"].keys()

    def test_create_physical_installation_subtype(
        self, client, base_physical_installation_subtype
    ):
        base_physical_installation_subtype[
            "name"
        ] = "SUBTIPO DE INSTALAÇÃO FÍSICA TESTE 1"
        response = client.post(
            "/physical_installation/subtype", json=base_physical_installation_subtype
        )

        assert response.json["message"] == "physical_installation_subtype_created"
        assert response.status_code == 201

    # --------------------- DELETE ---------------------
    def test_delete_physical_installation_subtype_with_invalid_id(self, client):
        response = client.delete("/physical_installation/subtype/0")

        assert response.json["message"] == "physical_installation_subtype_not_found"
        assert response.status_code == 404

    def test_delete_physical_installation_subtype(self, client):
        response = client.delete("/physical_installation/subtype/1")

        assert response.json["message"] == "physical_installation_subtype_deleted"
        assert response.status_code == 200
