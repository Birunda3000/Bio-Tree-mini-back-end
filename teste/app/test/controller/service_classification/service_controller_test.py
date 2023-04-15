import pytest

from app.main import db
from app.main.model import Service
from app.test.seeders import create_base_seed_classification, create_base_seed_service


@pytest.fixture(scope="module")
def seeded_database(client, database):
    """Seed database with prescription data"""

    create_base_seed_service(db)
    create_base_seed_classification(db)


@pytest.mark.usefixtures("seeded_database")
class TestServiceController:

    # --------------------- GET ---------------------

    def test_get_services(self, client):
        response = client.get("/service")

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 2
        assert response.json["total_pages"] == 1

        assert response.json["items"][0]["id"] == 1
        assert response.json["items"][0]["name"] == "SERVICE ONE"
        assert response.json["items"][1]["id"] == 2
        assert response.json["items"][1]["name"] == "SERVICE TWO"

    def test_get_services_by_name(self, client):
        response = client.get("/service", query_string={"name": "ONE"})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 1
        assert response.json["total_pages"] == 1

        assert response.json["items"][0]["id"] == 1
        assert response.json["items"][0]["name"] == "SERVICE ONE"

    def test_get_services_by_code(self, client):
        response = client.get("/service", query_string={"code": "002"})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 1
        assert response.json["total_pages"] == 1

        assert response.json["items"][0]["id"] == 2
        assert response.json["items"][0]["name"] == "SERVICE TWO"

    # --------------------- GET BY ID  ---------------------

    def test_get_service(self, client):
        response = client.get("/service/1")

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["id"] == 1
        assert response.json["code"] == "001"
        assert response.json["name"] == "SERVICE ONE"
        assert response.json["classifications"][0]["id"] == 1
        assert response.json["classifications"][0]["code"] == "001"
        assert response.json["classifications"][0]["name"] == "CLASSIFICATION ONE"
        assert response.json["classifications"][1]["id"] == 2
        assert response.json["classifications"][1]["code"] == "002"
        assert response.json["classifications"][1]["name"] == "CLASSIFICATION TWO"

    def test_get_service_that_not_exists(self, client):
        response = client.get("/service/0")

        assert response.status_code == 404
        assert response.json["message"] == "service_not_found"

    # --------------------- UPDATE ---------------------

    @pytest.mark.parametrize(
        "key, value",
        [
            ("code", "ABC"),
            ("name", 0),
        ],
        ids=["invalid_code", "invalid_name"],
    )
    def test_update_service_with_invalid_properties(
        self, client, base_service, key, value
    ):
        base_service[key] = value
        response = client.put("/service/1", json=base_service)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert key in response.json["errors"].keys()

    @pytest.mark.parametrize(
        "key_popped",
        [
            "code",
            "name",
        ],
        ids=["without_code", "without_name"],
    )
    def test_update_classification_without_required_properties(
        self, client, base_service, key_popped
    ):
        del base_service[key_popped]
        response = client.put("/service/1", json=base_service)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert key_popped in response.json["errors"].keys()

    def test_update_service_that_not_exists(self, client, base_service):
        response = client.put("/service/0", json=base_service)

        assert response.status_code == 404
        assert response.json["message"] == "service_not_found"

    @pytest.mark.parametrize(
        "key, value",
        [
            ("code", "002"),
            ("name", "SERVICE TWO"),
        ],
        ids=["registered_code", "registered_name"],
    )
    def test_update_service_with_registered_properties(
        self, client, base_service, key, value
    ):
        base_service[key] = value
        response = client.put("/service/1", json=base_service)

        assert response.status_code == 409
        assert response.json["message"] == f"{key}_in_use"

    def test_update_service(self, client, base_service):
        response = client.put("/service/1", json=base_service)

        assert response.status_code == 200
        assert response.json["message"] == "service_updated"

        self._undo_service_update_changes()

    # --------------------- POST ---------------------

    @pytest.mark.parametrize(
        "key_popped",
        [
            "code",
            "name",
        ],
        ids=["without_code", "without_name"],
    )
    def test_create_classification_without_required_properties(
        self, client, base_service, key_popped
    ):
        del base_service[key_popped]
        response = client.post("/service", json=base_service)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert key_popped in response.json["errors"].keys()

    @pytest.mark.parametrize(
        "key, value",
        [
            ("code", "ABC"),
            ("name", 0),
        ],
        ids=["invalid_code", "invalid_name"],
    )
    def test_create_service_with_invalid_properties(
        self, client, base_service, key, value
    ):
        base_service[key] = value
        response = client.post("/service", json=base_service)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert key in response.json["errors"].keys()

    @pytest.mark.parametrize(
        "key, value",
        [
            ("code", "001"),
            ("name", "SERVICE ONE"),
        ],
        ids=["registered_code", "registered_name"],
    )
    def test_create_service_with_registered_properties(
        self, client, base_service, key, value
    ):
        base_service[key] = value
        response = client.post("/service", json=base_service)

        assert response.status_code == 409
        assert response.json["message"] == f"{key}_in_use"

    def test_create_service(self, client, base_service):
        response = client.post("/service", json=base_service)

        assert response.status_code == 201
        assert response.json["message"] == "service_created"

    # --------------------- DELETE ---------------------

    def test_delete_service_with_non_registered_id(self, client):
        response = client.delete("/service/0")

        assert response.status_code == 404
        assert response.json["message"] == "service_not_found"

    def test_delete_service_with_classification_associated(self, client):
        response = client.delete("/service/1")

        assert response.status_code == 409
        assert response.json["message"] == "service_is_associated_with_classification"

    def test_delete_service(self, client):
        response = client.delete("/service/2")

        assert response.status_code == 200
        assert response.json["message"] == "service_deleted"

    # --------------------- Helper functions  ---------------------

    def _undo_service_update_changes(self) -> None:
        service = Service.query.get(1)

        service.service_id = 1
        service.code = "001"
        service.name = "SERVICE ONE"

        db.session.commit()
