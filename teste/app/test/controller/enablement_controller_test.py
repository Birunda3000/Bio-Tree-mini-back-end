import pytest

from app.main import db
from app.main.model import Enablement
from app.test.seeders import create_base_seed_enablement


@pytest.fixture(scope="module")
def seeded_database(client, database):
    """Seed database with prescription data"""

    return create_base_seed_enablement(db)


@pytest.mark.usefixtures("seeded_database")
class TestEnablementController:

    # --------------------- GET ---------------------

    def test_get_enablements(self, client):
        response = client.get("/enablement")

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 2
        assert response.json["total_pages"] == 1
        self._test_enablement_with_id_1_data(item=response.json["items"][0])

    @pytest.mark.parametrize(
        "parameter, value",
        [
            ("code", "0001"),
            ("code", "1"),
            ("name", "HABILITAÇÃO TESTE 1"),
            ("name", "1"),
        ],
        ids=[
            "complete_code",
            "incomplete_code",
            "complete_name",
            "incomplete_name",
        ],
    )
    def test_get_enablements_with_parameters(self, client, parameter, value):
        response = client.get("/enablement", query_string={parameter: value})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 1
        assert response.json["total_pages"] == 1
        self._test_enablement_with_id_1_data(item=response.json["items"][0])

    # --------------------- GET BY ID  ---------------------

    def test_get_enablement(self, client):
        response = client.get("/enablement/1")

        assert response.status_code == 200
        assert len(response.json) == 6
        self._test_enablement_with_id_1_data(item=response.json)

    def test_get_enablement_by_invalid_id(self, client):
        response = client.get("/enablement/0")

        assert response.status_code == 404
        assert response.json["message"] == "enablement_not_found"

    # --------------------- POST ---------------------

    @pytest.mark.parametrize(
        "key_popped",
        ["code", "name"],
        ids=["without_code", "without_name"],
    )
    def test_create_enablement_without_required_data(
        self, client, base_enablement, key_popped
    ):
        del base_enablement[key_popped]
        response = client.post("/enablement", json=base_enablement)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert key_popped in response.json["errors"].keys()

    @pytest.mark.parametrize(
        "key, value, message",
        [
            ("code", "0001", "code_in_use"),
            ("name", "HABILITAÇÃO TESTE 1", "name_in_use"),
        ],
        ids=["registered_code", "registered_name"],
    )
    def test_create_enablement_with_registered_data(
        self, client, base_enablement, key, value, message
    ):
        base_enablement[key] = value
        response = client.post("/enablement", json=base_enablement)

        assert response.status_code == 409
        assert response.json["message"] == message

    def test_create_enablement(self, client, base_enablement):
        response = client.post("/enablement", json=base_enablement)

        assert response.status_code == 201
        assert response.json["message"] == "enablement_created"
        self._test_enablement_name_saved_in_uppercase(id=3)

    @pytest.mark.parametrize(
        "key, id",
        [("number_of_beds", 4), ("ordinance_number", 5), ("release_date", 6)],
        ids=[
            "without_number_of_beds",
            "without_ordinance_number",
            "without_release_date",
        ],
    )
    def test_create_enablement_without_optional_data(
        self, client, base_enablement, key, id
    ):
        del base_enablement[key]
        base_enablement["name"] = f"Habilitação teste {id}"
        base_enablement["code"] = f"000{id}"
        response = client.post("/enablement", json=base_enablement)

        assert response.status_code == 201
        assert response.json["message"] == "enablement_created"
        self._test_enablement_name_saved_in_uppercase(id=id)

    # --------------------- DELETE ---------------------

    def test_delete_enablement_with_non_registered_id(self, client):
        response = client.delete("/enablement/0")

        assert response.status_code == 404
        assert response.json["message"] == "enablement_not_found"

    def test_delete_enablement(self, client):
        response = client.delete("/enablement/1")

        assert response.status_code == 200
        assert response.json["message"] == "enablement_deleted"

    # --------------------- Helper functions  ---------------------
    def _test_enablement_with_id_1_data(self, item: dict[str, any]) -> None:
        assert item["id"] == 1
        assert item["code"] == "0001"
        assert item["name"] == "HABILITAÇÃO TESTE 1"
        assert item["number_of_beds"] == 100
        assert item["ordinance_number"] == 1
        assert item["release_date"] == "01/01/1990"

    def _test_enablement_name_saved_in_uppercase(self, id: int) -> None:
        enablement = Enablement.query.get(id)

        assert enablement.name == f"HABILITAÇÃO TESTE {id}"
