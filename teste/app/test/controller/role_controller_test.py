import pytest

from app.main import db
from app.main.service import create_default_resources, create_default_roles
from app.test.seeders import create_base_seed_role


@pytest.fixture(scope="module")
def seeded_database(database):
    """Seed database with roles and resources"""
    create_default_resources()
    create_default_roles()
    create_base_seed_role(db)


@pytest.mark.usefixtures("seeded_database")
class TestRoleController:
    # --------------------- GET ROLES ---------------------

    def test_get_roles(self, client):
        response = client.get("/role")

        assert response.status_code == 200
        assert len(response.json) == 3
        assert response.json[0]["name"] == "Administrador"

    def teste_get_roles_by_name(self, client):
        response = client.get("/role", query_string={"name": "Enfermeira"})

        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]["name"] == "Enfermeira"

    # --------------------- UPDATE ROLE ---------------------

    def test_update_role_with_invalid_id(self, client):
        response = client.put(
            "/role/99", json={"name": "Testeput", "resources": ["atendimento"]}
        )

        assert response.status_code == 404
        assert response.json["message"] == "role_not_found"

    def test_update_role_with_registered_name(self, client):
        response = client.put(
            "/role/2", json={"name": "Enfermeira", "resources": ["atendimento"]}
        )

        assert response.status_code == 409
        assert response.json["message"] == "role_in_use"

    def test_update_role_with_empty_resource_list(self, client):
        response = client.put("/role/2", json={"name": "Médico", "resources": []})

        assert response.status_code == 400
        assert "resources" in response.json["errors"].keys()
        assert response.json["message"] == "resource_invalid"

    def test_update_role_with_invalid_resource_name(self, client):
        response = client.put(
            "/role/2", json={"name": "Médico", "resources": ["invalidresource"]}
        )

        assert response.status_code == 400
        assert "resources.0" in response.json["errors"].keys()
        assert response.json["message"] == "Input payload validation failed"

    def test_update_default_role(self, client):
        response = client.put(
            "/role/1", json={"name": "Teste", "resources": ["atendimento"]}
        )

        assert response.status_code == 409
        assert response.json["message"] == "role_is_default"

    def test_update_role_with_empty_name(self, client):
        response = client.put(
            "/role/2", json={"name": "", "resources": ["atendimento"]}
        )

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert "name" in response.json["errors"].keys()

    def test_update_role(self, client):
        response = client.put(
            "/role/2", json={"name": "Testeput", "resources": ["atendimento"]}
        )

        assert response.status_code == 200
        assert response.json["message"] == "role_updated"

    # --------------------- CREATE ROLE ---------------------

    def test_create_role_with_registered_name(self, client):
        response = client.post(
            "/role", json={"name": "Enfermeira", "resources": ["atendimento"]}
        )

        assert response.status_code == 409
        assert response.json["message"] == "role_in_use"

    def test_create_role_with_empty_resource_list(self, client):
        response = client.post("/role", json={"name": "Enfermeira", "resources": []})

        assert response.status_code == 400
        assert "resources" in response.json["errors"].keys()
        assert response.json["message"] == "resource_invalid"

    def test_create_role_with_invalid_resource_name(self, client):
        response = client.post(
            "/role", json={"name": "Médico", "resources": ["invalidresource"]}
        )
        assert response.status_code == 400
        assert "resources.0" in response.json["errors"].keys()
        assert response.json["message"] == "Input payload validation failed"

    def test_create_role_with_empty_name(self, client):
        response = client.post("/role", json={"name": "", "resources": ["atendimento"]})

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert "name" in response.json["errors"].keys()

    @pytest.mark.parametrize(
        "role_name, resources",
        [
            ("Role1", ["atendimento"]),
            ("Role2", ["gerenciamentodepaciente"]),
            ("Role3", ["atendimento", "gerenciamentodepaciente"]),
        ],
        ids=["only_attendance_resource", "only_management_resource", "both_resources"],
    )
    def test_create_role(self, client, role_name, resources):
        response = client.post(
            "/role", json={"name": role_name, "resources": resources}
        )

        assert response.status_code == 201
        assert response.json["message"] == "role_created"

    # --------------------- DELETE ROLE ---------------------

    def test_delete_role_with_invalid_id(self, client):
        response = client.delete("/role/0")

        assert response.status_code == 404
        assert response.json["message"] == "role_not_found"

    def test_delete_default_role(self, client):
        response = client.delete("/role/1")

        assert response.status_code == 409
        assert response.json["message"] == "role_is_default"

    def test_delete_non_default_role(self, client):
        response = client.delete("/role/2")

        assert response.status_code == 200
        assert response.json["message"] == "role_deleted"
