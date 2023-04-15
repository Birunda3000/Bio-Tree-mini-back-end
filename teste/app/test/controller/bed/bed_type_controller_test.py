import pytest

from app.main import db
from app.main.model import BedType
from app.test.seeders import create_base_seed_bed_type


@pytest.fixture(scope="module")
def seeded_database(client, database):
    """Seed database with bed type data"""

    return create_base_seed_bed_type(db)


@pytest.mark.usefixtures("seeded_database")
class TestBedTypeController:

    # --------------------- GET ---------------------

    def test_get_bed_types(self, client):
        response = client.get("/bed/type")

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 2
        assert response.json["total_pages"] == 1
        self._test_bed_type_with_id_1_data(item=response.json["items"][0])

    @pytest.mark.parametrize(
        "parameter, value",
        [
            ("name", "tipo de leito teste 1"),
            ("name", "1"),
        ],
        ids=[
            "complete_name",
            "incomplete_name",
        ],
    )
    def test_get_bed_types_with_parameters(self, client, parameter, value):
        response = client.get("/bed/type", query_string={parameter: value})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 1
        assert response.json["total_pages"] == 1
        self._test_bed_type_with_id_1_data(item=response.json["items"][0])

    # --------------------- GET BY ID  ---------------------

    def test_get_bed_type_by_id(self, client):
        response = client.get("/bed/type/1")

        assert response.status_code == 200
        assert len(response.json) == 2
        self._test_bed_type_with_id_1_data(item=response.json)

    def test_get_bed_type_by_invalid_id(self, client):
        response = client.get("/bed/type/0")

        assert response.status_code == 404
        assert response.json["message"] == "bed_type_not_found"

    # --------------------- UPDATE ---------------------

    @pytest.mark.parametrize(
        "key_popped",
        ["name"],
        ids=["without_name"],
    )
    def test_update_bed_type_without_required_data(
        self, client, base_bed_type, key_popped
    ):
        del base_bed_type[key_popped]
        response = client.put("/bed/type/1", json=base_bed_type)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert key_popped in response.json["errors"].keys()

    @pytest.mark.parametrize(
        "key, value, message",
        [
            ("name", "tipo de leito teste 1", "name_in_use"),
        ],
        ids=["registered_name"],
    )
    def test_update_bed_type_with_registered_data(
        self, client, base_bed_type, key, value, message
    ):
        base_bed_type[key] = value
        response = client.put("/bed/type/2", json=base_bed_type)

        assert response.status_code == 409
        assert response.json["message"] == message

    def test_update_bed_type(self, client, base_bed_type):
        response = client.put("/bed/type/1", json=base_bed_type)

        assert response.status_code == 200
        assert response.json["message"] == "bed_type_updated"

        self._undo_bed_type_update_changes()

    # --------------------- POST ---------------------

    @pytest.mark.parametrize(
        "key_popped",
        ["name"],
        ids=["without_name"],
    )
    def test_create_bed_type_without_required_data(
        self, client, base_bed_type, key_popped
    ):
        del base_bed_type[key_popped]
        response = client.post("/bed/type", json=base_bed_type)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert key_popped in response.json["errors"].keys()

    @pytest.mark.parametrize(
        "key, value, message",
        [
            ("name", "tipo de leito teste 1", "name_in_use"),
        ],
        ids=["registered_name"],
    )
    def test_create_bed_type_with_registered_data(
        self, client, base_bed_type, key, value, message
    ):
        base_bed_type[key] = value
        response = client.post("/bed/type", json=base_bed_type)

        assert response.status_code == 409
        assert response.json["message"] == message

    def test_create_bed_type(self, client, base_bed_type):
        response = client.post("/bed/type", json=base_bed_type)

        assert response.status_code == 201
        assert response.json["message"] == "bed_type_created"

    # --------------------- DELETE ---------------------

    def test_delete_bed_type(self, client):
        response = client.delete("/bed/type/1")

        assert response.status_code == 200
        assert response.json["message"] == "bed_type_deleted"

    def test_delete_bed_type_with_non_registered_id(self, client):
        response = client.delete("/bed/type/0")

        assert response.status_code == 404
        assert response.json["message"] == "bed_type_not_found"

    # --------------------- Helper functions  ---------------------

    def _test_bed_type_with_id_1_data(self, item: dict[str, any]) -> None:
        assert item["id"] == 1
        assert item["name"] == "TIPO DE LEITO TESTE 1"

    def _undo_bed_type_update_changes(self):
        bed_type = BedType.query.get(1)

        bed_type.name = "TIPO DE LEITO TESTE 1"

        db.session.add(bed_type)
        db.session.commit()
