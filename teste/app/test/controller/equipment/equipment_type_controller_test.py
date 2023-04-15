import pytest

from app.main import db
from app.test.seeders.equipment import (
    create_base_seed_equipment,
    create_base_seed_equipment_type,
)


@pytest.fixture(scope="module")
def seeded_database(client, database):
    """Seed database with equipment and equipment type data"""

    create_base_seed_equipment_type(db)
    return create_base_seed_equipment(db)


@pytest.mark.usefixtures("seeded_database")
class TestEquipmentTypeController:

    # --------------------- GET ---------------------

    def test_get_equipment_types(self, client):
        response = client.get("/equipment/type")

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 2
        assert response.json["total_pages"] == 1

        assert response.json["items"][0]["id"] == 1
        assert response.json["items"][0]["name"] == "TIPO DE EQUIPAMENTO TESTE 1"
        assert response.json["items"][1]["id"] == 2
        assert response.json["items"][1]["name"] == "TIPO DE EQUIPAMENTO TESTE 2"

    @pytest.mark.parametrize(
        "name",
        ["1", "tipo de equipamento teste 1"],
        ids=["incomplete", "complete"],
    )
    def test_get_equipment_types_by_name(self, client, name):
        response = client.get("/equipment/type", query_string={"name": name})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 1
        assert response.json["total_pages"] == 1

        assert response.json["items"][0]["id"] == 1
        assert response.json["items"][0]["name"] == "TIPO DE EQUIPAMENTO TESTE 1"

    # --------------------- PUT ---------------------

    @pytest.mark.parametrize(
        "key_popped",
        ["name"],
        ids=["name"],
    )
    def test_update_equipment_type_without_required_data(
        self, client, base_equipment_type, key_popped
    ):
        base_equipment_type.pop(key_popped)
        response = client.put("/equipment/type/1", json=base_equipment_type)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert key_popped in response.json["errors"].keys()

    def test_update_equipment_type_by_invalid_id(self, client, base_equipment_type):
        response = client.put("/equipment/type/0", json=base_equipment_type)

        assert response.status_code == 404
        assert response.json["message"] == "equipment_type_not_found"

    def test_update_equipment_type_with_registered_name(
        self, client, base_equipment_type
    ):
        base_equipment_type["name"] = "tipo de equipamento teste 2"
        response = client.put("/equipment/type/1", json=base_equipment_type)

        assert response.status_code == 409
        assert response.json["message"] == "name_in_use"

    def test_update_equipment_type(self, client, base_equipment_type):
        base_equipment_type["name"] = "tipo de equipamento teste atualizado"
        response = client.put("/equipment/type/1", json=base_equipment_type)

        assert response.status_code == 200
        assert response.json["message"] == "equipment_type_updated"

    # --------------------- POST ---------------------

    @pytest.mark.parametrize(
        "key_popped",
        ["name"],
        ids=["name"],
    )
    def test_create_equipment_type_without_required_data(
        self, client, base_equipment_type, key_popped
    ):
        base_equipment_type.pop(key_popped)
        response = client.post("/equipment/type", json=base_equipment_type)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert key_popped in response.json["errors"].keys()

    def test_create_equipment_type_with_registered_name(
        self, client, base_equipment_type
    ):
        base_equipment_type["name"] = "tipo de equipamento teste atualizado"
        response = client.post("/equipment/type", json=base_equipment_type)

        assert response.status_code == 409
        assert response.json["message"] == "name_in_use"

    def test_create_equipment_type(self, client, base_equipment_type):
        response = client.post("/equipment/type", json=base_equipment_type)

        assert response.status_code == 201
        assert response.json["message"] == "equipment_type_created"

    # --------------------- DELETE ---------------------

    def test_delete_equipment_type_with_non_registered_id(self, client):
        response = client.delete("/equipment/type/0")

        assert response.status_code == 404
        assert response.json["message"] == "equipment_type_not_found"

    def test_delete_equipment_type_associated_with_equipment(self, client):
        response = client.delete("/equipment/type/1")

        assert response.status_code == 409
        assert response.json["message"] == "equipment_type_is_associated_with_equipment"

    def test_delete_equipment_type(self, client):
        response = client.delete("/equipment/type/2")

        assert response.status_code == 200
        assert response.json["message"] == "equipment_type_deleted"
