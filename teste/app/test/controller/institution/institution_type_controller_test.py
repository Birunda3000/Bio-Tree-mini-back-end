import pytest

from app.main import db
from app.test.seeders import (
    create_base_seed_institution_subtype,
    create_base_seed_institution_type,
)


@pytest.fixture(scope="module")
def seeded_database(client, database):
    """Seed database with prescription data"""

    create_base_seed_institution_type(db)
    create_base_seed_institution_subtype(db)


@pytest.mark.usefixtures("seeded_database")
class TestInstitutionTypeController:

    # --------------------- GET ---------------------

    def test_get_institution_types(self, client):
        response = client.get("/institution/type")

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 3
        assert response.json["total_pages"] == 1

        assert response.json["items"][0]["id"] == 1
        assert response.json["items"][0]["name"] == "INSTITUTION TYPE ONE"
        assert response.json["items"][1]["id"] == 2
        assert response.json["items"][1]["name"] == "INSTITUTION TYPE TWO"

    def test_get_institution_types_by_name(self, client):
        response = client.get("/institution/type", query_string={"name": "one"})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 1
        assert response.json["total_pages"] == 1

        assert response.json["items"][0]["id"] == 1
        assert response.json["items"][0]["name"] == "INSTITUTION TYPE ONE"

    # --------------------- GET BY ID ---------------------

    def test_get_institution_type(self, client):
        response = client.get("/institution/type/1")

        assert response.status_code == 200
        assert len(response.json) == 3
        assert response.json["id"] == 1
        assert response.json["name"] == "INSTITUTION TYPE ONE"
        assert response.json["institution_subtypes"][0]["id"] == 1
        assert (
            response.json["institution_subtypes"][0]["name"]
            == "INSTITUTION SUBTYPE ONE"
        )
        assert response.json["institution_subtypes"][0]["institution_type_id"] == 1

    def test_get_institution_type_that_not_exists(self, client):
        response = client.get("/institution/type/0")

        assert response.status_code == 404
        assert response.json["message"] == "institution_type_not_found"

    # --------------------- UPDATE ---------------------

    def test_update_institution_subtype_without_required_data(
        self, client, base_institution_type
    ):
        base_institution_type.pop("name", None)
        response = client.put("/institution/type/1", json=base_institution_type)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"

    def test_update_institution_type_with_invalid_data(
        self, client, base_institution_type
    ):
        base_institution_type["name"] = 0
        response = client.put("/institution/type/1", json=base_institution_type)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"

    def test_update_institution_type_that_not_exists(
        self, client, base_institution_type
    ):
        response = client.put("/institution/type/0", json=base_institution_type)

        assert response.status_code == 404
        assert response.json["message"] == "institution_type_not_found"

    def test_update_institution_type_with_registered_name(
        self, client, base_institution_type
    ):
        base_institution_type["name"] = "INSTITUTION TYPE TWO"
        response = client.put("/institution/type/1", json=base_institution_type)

        assert response.status_code == 409
        assert response.json["message"] == "name_in_use"

    def test_update_institution_type(self, client, base_institution_type):
        response = client.put("/institution/type/1", json=base_institution_type)

        assert response.status_code == 200
        assert response.json["message"] == "institution_type_updated"

    # --------------------- POST ---------------------

    def test_create_institution_subtype_without_required_data(
        self, client, base_institution_type
    ):
        base_institution_type.pop("name", None)
        response = client.post("/institution/type", json=base_institution_type)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"

    def test_create_institution_type_with_invalid_data(
        self, client, base_institution_type
    ):
        base_institution_type["name"] = 0
        response = client.post("/institution/type", json=base_institution_type)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"

    def test_create_institution_type_with_registered_name(
        self, client, base_institution_type
    ):
        response = client.post("/institution/type", json=base_institution_type)

        assert response.status_code == 409
        assert response.json["message"] == "name_in_use"

    def test_create_institution_type(self, client, base_institution_type):
        base_institution_type["name"] = "INSTITUTION TYPE POST"

        response = client.post("/institution/type", json=base_institution_type)

        assert response.status_code == 201
        assert response.json["message"] == "institution_type_created"

    # --------------------- DELETE ---------------------

    def test_delete_institution_type_with_non_registered_id(self, client):
        response = client.delete("/institution/type/0")

        assert response.status_code == 404
        assert response.json["message"] == "institution_type_not_found"

    def test_delete_institution_type_with_subtypes_associated(self, client):
        response = client.delete("/institution/type/1")

        assert response.status_code == 409
        assert response.json["message"] == "institution_type_is_associated_with_subtype"

    def test_delete_institution_type(self, client):
        response = client.delete("/institution/type/2")

        assert response.status_code == 200
        assert response.json["message"] == "institution_type_deleted"
