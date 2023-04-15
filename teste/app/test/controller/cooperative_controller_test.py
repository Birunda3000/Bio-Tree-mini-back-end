import pytest

from app.main import db
from app.main.model import Cooperative
from app.test.seeders import create_base_seed_cooperative


@pytest.fixture(scope="module")
def seeded_database(client, database):
    """Seed database with cooperative data"""

    return create_base_seed_cooperative(db)


@pytest.mark.usefixtures("seeded_database")
class TestCooperativeController:

    # --------------------- GET ---------------------

    def test_get_cooperatives(self, client):
        response = client.get("/cooperative")

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 2
        assert response.json["total_pages"] == 1
        self._test_cooperative_with_id_1_data(item=response.json["items"][0])

    @pytest.mark.parametrize(
        "parameter, value",
        [
            ("cbo", "CBO1"),
            ("cbo", "1"),
        ],
        ids=[
            "complete_cbo",
            "incomplete_cbo",
        ],
    )
    def test_get_cooperatives_with_parameters(self, client, parameter, value):
        response = client.get("/cooperative", query_string={parameter: value})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 1
        assert response.json["total_pages"] == 1
        self._test_cooperative_with_id_1_data(item=response.json["items"][0])

    # --------------------- GET BY ID  ---------------------

    def test_cooperative(self, client):
        response = client.get("/cooperative/1")

        assert response.status_code == 200
        assert len(response.json) == 3
        self._test_cooperative_with_id_1_data(item=response.json)

    def test_get_cooperative_by_invalid_id(self, client):
        response = client.get("/cooperative/0")

        assert response.status_code == 404
        assert response.json["message"] == "cooperative_not_found"

    # --------------------- UPDATE  ---------------------

    def test_update_cooperative_with_invalid_id(self, client, base_cooperative):
        response = client.put("/cooperative/0", json=base_cooperative)

        assert response.status_code == 404
        assert response.json["message"] == "cooperative_not_found"

    @pytest.mark.parametrize(
        "key_popped",
        [
            "name",
            "cbo",
        ],
        ids=[
            "without_name",
            "without_cbo",
        ],
    )
    def test_update_cooperative_without_required_data(
        self, client, base_cooperative, key_popped
    ):
        del base_cooperative[key_popped]
        response = client.put("/cooperative/1", json=base_cooperative)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert key_popped in response.json["errors"].keys()

    @pytest.mark.parametrize(
        "key, value, message",
        [
            ("cbo", "CBO2", "cbo_in_use"),
        ],
        ids=[
            "registered_cbo",
        ],
    )
    def test_update_cooperative_with_registered_data(
        self, client, base_cooperative, key, value, message
    ):
        base_cooperative[key] = value
        response = client.put("/cooperative/1", json=base_cooperative)

        assert response.status_code == 409
        assert response.json["message"] == message

    def test_update_cooperative(self, client, base_cooperative):
        base_cooperative["cbo"] = "CBO4"
        response = client.put("/cooperative/2", json=base_cooperative)

        assert response.status_code == 200
        assert response.json["message"] == "cooperative_updated"
        self._test_cooperative_cbo_saved_in_uppercase(id=2, cbo_number=4)

    # --------------------- POST ---------------------

    @pytest.mark.parametrize(
        "key_popped",
        [
            "name",
            "cbo",
        ],
        ids=[
            "without_name",
            "without_cbo",
        ],
    )
    def test_create_cooperative_without_required_data(
        self, client, base_cooperative, key_popped
    ):
        del base_cooperative[key_popped]
        response = client.post("/cooperative", json=base_cooperative)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert key_popped in response.json["errors"].keys()

    @pytest.mark.parametrize(
        "key, value, message",
        [
            ("cbo", "CBO1", "cbo_in_use"),
        ],
        ids=[
            "registered_cbo",
        ],
    )
    def test_create_cooperative_with_registered_data(
        self, client, base_cooperative, key, value, message
    ):
        base_cooperative[key] = value
        response = client.post("/cooperative", json=base_cooperative)

        assert response.status_code == 409
        assert response.json["message"] == message

    def test_create_cooperative(self, client, base_cooperative):
        response = client.post("/cooperative", json=base_cooperative)

        assert response.status_code == 201
        assert response.json["message"] == "cooperative_created"
        self._test_cooperative_cbo_saved_in_uppercase(id=3, cbo_number=3)

    # --------------------- DELETE ---------------------

    def test_delete_cooperative_with_non_registered_id(self, client):
        response = client.delete("/cooperative/0")

        assert response.status_code == 404
        assert response.json["message"] == "cooperative_not_found"

    def test_delete_cooperative(self, client):
        response = client.delete("/cooperative/1")

        assert response.status_code == 200
        assert response.json["message"] == "cooperative_deleted"

    # --------------------- Helper functions  ---------------------

    def _test_cooperative_with_id_1_data(self, item: dict[str, any]) -> None:
        assert item["id"] == 1
        assert item["name"] == "Cooperativa teste 1"
        assert item["cbo"] == "CBO1"

    def _test_cooperative_cbo_saved_in_uppercase(
        self, id: int, cbo_number: int
    ) -> None:
        cooperative = Cooperative.query.get(id)

        assert cooperative.cbo == f"CBO{cbo_number}"
