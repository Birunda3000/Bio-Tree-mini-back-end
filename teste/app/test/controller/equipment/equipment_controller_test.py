import pytest

from app.main import db
from app.test.seeders.equipment import (
    create_base_seed_equipment,
    create_base_seed_equipment_type,
)


@pytest.fixture(scope="module")
def seeded_database(client, database):
    """Seed database with equipment data"""

    create_base_seed_equipment_type(db)
    return create_base_seed_equipment(db)


@pytest.mark.usefixtures("seeded_database")
class TestEquipmentController:

    # --------------------- GET ---------------------

    def test_get_equipments(self, client):
        response = client.get("/equipment")

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 2
        assert response.json["total_pages"] == 1
        self._test_equipment_id_1_data(data=response.json["items"][0])

    @pytest.mark.parametrize(
        "name",
        ["1", "equipamento teste 1"],
        ids=["incomplete", "complete"],
    )
    def test_get_equipments_by_name(self, client, name):
        response = client.get("/equipment", query_string={"name": name})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 1
        assert response.json["total_pages"] == 1
        self._test_equipment_id_1_data(data=response.json["items"][0])

    # --------------------- GET BY ID ---------------------

    def test_get_equipment_by_id(self, client):
        response = client.get("/equipment/1")

        assert response.status_code == 200
        self._test_equipment_id_1_data(data=response.json)

    def test_get_equipment_by_non_registered_id(self, client):
        response = client.get("/equipment/0")

        assert response.status_code == 404
        assert response.json["message"] == "equipment_not_found"

    # --------------------- POST ---------------------

    @pytest.mark.parametrize(
        "key_popped",
        ["name", "equipment_type_id"],
        ids=["name", "equipment type id"],
    )
    def test_create_equipment_without_required_data(
        self, client, base_equipment, key_popped
    ):
        base_equipment.pop(key_popped)
        response = client.post("/equipment", json=base_equipment)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert key_popped in response.json["errors"].keys()

    def test_create_equipment_with_registered_name(self, client, base_equipment):
        base_equipment["name"] = "equipamento teste 1"
        response = client.post("/equipment", json=base_equipment)

        assert response.status_code == 409
        assert response.json["message"] == "name_in_use"

    def test_create_equipment_with_non_registered_type_id(self, client, base_equipment):
        base_equipment["equipment_type_id"] = 0
        response = client.post("/equipment", json=base_equipment)

        assert response.status_code == 404
        assert response.json["message"] == "equipment_type_not_found"

    def test_create_equipment(self, client, base_equipment):
        response = client.post("/equipment", json=base_equipment)

        assert response.status_code == 201
        assert response.json["message"] == "equipment_created"

    # --------------------- DELETE ---------------------

    def test_delete_prescription_with_non_registered_id(self, client):
        response = client.delete("/equipment/0")

        assert response.status_code == 404
        assert response.json["message"] == "equipment_not_found"

    def test_delete_equipment(self, client):
        response = client.delete("/equipment/1")

        assert response.status_code == 200
        assert response.json["message"] == "equipment_deleted"

    # --------------------- Helper Functions ---------------------
    def _test_equipment_id_1_data(self, data: dict[str, any]) -> None:
        assert data["id"] == 1
        assert data["name"] == "EQUIPAMENTO TESTE 1"
        assert data["equipment_type"] == {
            "id": 1,
            "name": "TIPO DE EQUIPAMENTO TESTE 1",
        }
