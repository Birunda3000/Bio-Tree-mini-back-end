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
class TestInstitutionSubtypeController:

    # --------------------- GET  ---------------------

    def test_get_institution_subtypes(self, client):
        response = client.get("/institution/subtype")

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 3
        assert response.json["total_pages"] == 1

        assert response.json["items"][0]["id"] == 1
        assert response.json["items"][0]["institution_type_id"] == 1
        assert response.json["items"][0]["name"] == "INSTITUTION SUBTYPE ONE"
        assert response.json["items"][1]["id"] == 2
        assert response.json["items"][1]["institution_type_id"] == 1
        assert response.json["items"][1]["name"] == "INSTITUTION SUBTYPE TWO"

    @pytest.mark.parametrize(
        "key, value",
        [
            ("institution_type_id", 3),
            ("name", "three"),
        ],
        ids=[
            "by_institution_type_id",
            "by_name",
        ],
    )
    def test_get_institution_subtypes_by_parameters(self, client, key, value):
        response = client.get("/institution/subtype", query_string={key: value})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 1
        assert response.json["total_pages"] == 1

        assert response.json["items"][0]["id"] == 3
        assert response.json["items"][0]["institution_type_id"] == 3
        assert response.json["items"][0]["name"] == "INSTITUTION SUBTYPE THREE"

    # --------------------- GET BY ID ---------------------

    def test_get_institution_subtype(self, client):
        response = client.get("/institution/subtype/1")

        assert response.status_code == 200
        assert len(response.json) == 3
        assert response.json["id"] == 1
        assert response.json["institution_type_id"] == 1
        assert response.json["name"] == "INSTITUTION SUBTYPE ONE"

    def test_get_institution_subtype_that_not_exists(self, client):
        response = client.get("/institution/subtype/0")

        assert response.status_code == 404
        assert response.json["message"] == "institution_subtype_not_found"

    # --------------------- UPDATE ---------------------

    @pytest.mark.parametrize(
        "key_popped",
        [
            "institution_type_id",
            "name",
        ],
        ids=[
            "update_without_institution_type_id",
            "update_without_name",
        ],
    )
    def test_update_institution_subtype_without_required_data(
        self, client, base_institution_subtype, key_popped
    ):
        base_institution_subtype.pop(key_popped, None)
        response = client.put("/institution/subtype/2", json=base_institution_subtype)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert key_popped in response.json["errors"].keys()

    def test_update_institution_subtype_with_invalid_data(
        self, client, base_institution_subtype
    ):
        base_institution_subtype["name"] = 0
        response = client.put("/institution/subtype/1", json=base_institution_subtype)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"

    def test_update_institution_subtype_that_not_exists(
        self, client, base_institution_subtype
    ):
        response = client.put("/institution/subtype/0", json=base_institution_subtype)

        assert response.status_code == 404
        assert response.json["message"] == "institution_subtype_not_found"

    def test_update_institution_subtype_with_invalid_institution_type(
        self, client, base_institution_subtype
    ):
        base_institution_subtype["institution_type_id"] = 0
        response = client.put("/institution/subtype/1", json=base_institution_subtype)

        assert response.status_code == 404
        assert response.json["message"] == "institution_type_not_found"

    def test_update_institution_subtype_with_same_type_id_and_registered_name(
        self, client, base_institution_subtype
    ):
        base_institution_subtype["name"] = "INSTITUTION SUBTYPE TWO"
        response = client.put("/institution/subtype/1", json=base_institution_subtype)

        assert response.status_code == 409
        assert response.json["message"] == "name_in_use"

    def test_update_institution_subtype_with_diff_type_id_and_registered_name(
        self, client, base_institution_subtype
    ):
        base_institution_subtype["institution_type_id"] = 2
        base_institution_subtype["name"] = "INSTITUTION SUBTYPE TWO"
        response = client.put("/institution/subtype/1", json=base_institution_subtype)

        assert response.status_code == 200
        assert response.json["message"] == "institution_subtype_updated"

    def test_update_institution_subtype(self, client, base_institution_subtype):
        response = client.put("/institution/subtype/1", json=base_institution_subtype)

        assert response.status_code == 200
        assert response.json["message"] == "institution_subtype_updated"

    # --------------------- POST ---------------------

    @pytest.mark.parametrize(
        "key_popped",
        [
            "institution_type_id",
            "name",
        ],
        ids=[
            "create_without_institution_type_id",
            "create_without_name",
        ],
    )
    def test_create_institution_subtype_without_required_data(
        self, client, base_institution_subtype, key_popped
    ):
        base_institution_subtype.pop(key_popped, None)
        response = client.post("/institution/subtype", json=base_institution_subtype)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert key_popped in response.json["errors"].keys()

    def test_create_institution_subtype_with_invalid_data(
        self, client, base_institution_subtype
    ):
        base_institution_subtype["name"] = 0
        response = client.post("/institution/subtype", json=base_institution_subtype)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"

    def test_create_institution_subtype_with_registered_name(
        self, client, base_institution_subtype
    ):
        response = client.post("/institution/subtype", json=base_institution_subtype)

        assert response.status_code == 409
        assert response.json["message"] == "name_in_use"

    def test_create_institution_subtype_with_invalid_institution_type(
        self, client, base_institution_subtype
    ):
        base_institution_subtype["institution_type_id"] = 0
        response = client.post("/institution/subtype", json=base_institution_subtype)

        assert response.status_code == 404
        assert response.json["message"] == "institution_type_not_found"

    def test_create_institution_subtype_with_same_type_id_and_registered_name(
        self, client, base_institution_subtype
    ):
        base_institution_subtype["name"] = "INSTITUTION SUBTYPE TWO"
        response = client.post("/institution/subtype", json=base_institution_subtype)

        assert response.status_code == 409
        assert response.json["message"] == "name_in_use"

    def test_create_institution_subtype(self, client, base_institution_subtype):
        base_institution_subtype["name"] = "INSTITUTION SUBTYPE POST"
        response = client.post("/institution/subtype", json=base_institution_subtype)

        assert response.status_code == 201
        assert response.json["message"] == "institution_subtype_created"

    def test_create_institution_subtype_with_diff_type_id_and_registered_name(
        self, client, base_institution_subtype
    ):
        base_institution_subtype["institution_type_id"] = 2
        base_institution_subtype["name"] = "INSTITUTION SUBTYPE POST"
        response = client.post("/institution/subtype", json=base_institution_subtype)

        assert response.status_code == 201
        assert response.json["message"] == "institution_subtype_created"

    # --------------------- DELETE ---------------------

    def test_delete_institution_subtype(self, client):
        response = client.delete("/institution/subtype/1")

        assert response.status_code == 200
        assert response.json["message"] == "institution_subtype_deleted"

    def test_delete_institution_with_non_registered_id(self, client):
        response = client.delete("/institution/subtype/0")

        assert response.status_code == 404
        assert response.json["message"] == "institution_subtype_not_found"
