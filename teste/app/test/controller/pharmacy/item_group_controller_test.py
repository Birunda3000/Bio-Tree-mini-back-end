import pytest

from app.main import db
from app.main.model import ItemGroup
from app.test.seeders import create_base_seed_item_group


@pytest.fixture(scope="module")
def seeded_database(client, database):
    """Seed database with prescription data"""

    create_base_seed_item_group(db)


@pytest.mark.usefixtures("seeded_database")
class TestItemGroupController:

    # --------------------- GET  ---------------------

    def test_get_item_groups(self, client):
        response = client.get("/item_group")

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 3
        assert response.json["total_pages"] == 1
        assert response.json["items"][0]["id"] == 1
        assert response.json["items"][0]["name"] == "ITEM GROUP 1"
        assert response.json["items"][1]["id"] == 2
        assert response.json["items"][1]["name"] == "ITEM GROUP 2"
        assert response.json["items"][2]["id"] == 3
        assert response.json["items"][2]["name"] == "ITEM GROUP 3"

    def test_get_item_groups_by_name(self, client):
        response = client.get("/item_group", query_string={"name": "1"})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 1
        assert response.json["total_pages"] == 1
        assert response.json["items"][0]["id"] == 1
        assert response.json["items"][0]["name"] == "ITEM GROUP 1"

    # --------------------- GET BY ID ---------------------

    def test_get_item_group(self, client):
        response = client.get("/item_group/1")

        assert response.status_code == 200
        assert len(response.json) == 2
        assert response.json["id"] == 1
        assert response.json["name"] == "ITEM GROUP 1"

    def test_get_item_group_that_not_exists(self, client):
        response = client.get("/item_group/0")

        assert response.json["message"] == "item_group_not_found"
        assert response.status_code == 404

    # --------------------- UPDATE ---------------------

    @pytest.mark.parametrize(
        "key_popped",
        [
            "name",
        ],
        ids=[
            "update_without_name",
        ],
    )
    def test_update_item_group_without_required_data(
        self, client, base_item_group, key_popped
    ):
        base_item_group.pop(key_popped, None)
        response = client.put("/item_group/2", json=base_item_group)

        assert response.json["message"] == "Input payload validation failed"
        assert response.status_code == 400
        assert key_popped in response.json["errors"].keys()

    @pytest.mark.parametrize(
        "key, value",
        [
            ("name", 0),
            ("name", ""),
        ],
        ids=[
            "with_invalid_name",
            "with_empty_name",
        ],
    )
    def test_update_item_group_with_invalid_data(
        self, client, base_item_group, key, value
    ):
        base_item_group[key] = value
        response = client.put("/item_group/1", json=base_item_group)

        assert response.json["message"] == "Input payload validation failed"
        assert response.status_code == 400
        assert key in response.json["errors"].keys()

    def test_update_item_group_that_not_exists(self, client, base_item_group):
        response = client.put("/item_group/0", json=base_item_group)

        assert response.json["message"] == "item_group_not_found"
        assert response.status_code == 404

    def test_update_item_group(self, client, base_item_group):
        response = client.put("/item_group/1", json=base_item_group)

        assert response.json["message"] == "item_group_updated"
        assert response.status_code == 200

        item_group = ItemGroup.query.get(1)

        for key in base_item_group.keys():
            assert getattr(item_group, key) == base_item_group.get(key)

    # --------------------- POST ---------------------

    @pytest.mark.parametrize(
        "key_popped",
        [
            "name",
        ],
        ids=[
            "create_without_name",
        ],
    )
    def test_create_item_group_without_required_data(
        self, client, base_item_group, key_popped
    ):
        base_item_group.pop(key_popped, None)
        response = client.post("/item_group", json=base_item_group)

        assert response.json["message"] == "Input payload validation failed"
        assert response.status_code == 400
        assert key_popped in response.json["errors"].keys()

    @pytest.mark.parametrize(
        "key, value",
        [
            ("name", 0),
            ("name", ""),
        ],
        ids=[
            "with_invalid_name",
            "with_empty_name",
        ],
    )
    def test_create_item_group_with_invalid_data(
        self, client, base_item_group, key, value
    ):
        base_item_group[key] = value
        response = client.post("/item_group", json=base_item_group)

        assert response.json["message"] == "Input payload validation failed"
        assert response.status_code == 400
        assert key in response.json["errors"].keys()

    def test_create_item_group_with_registered_name(self, client, base_item_group):
        response = client.post("/item_group", json=base_item_group)

        assert response.json["message"] == "name_in_use"
        assert response.status_code == 409

    def test_create_item_group(self, client, base_item_group):
        base_item_group["name"] = "ITEM GROUP POST"
        response = client.post("/item_group", json=base_item_group)

        assert response.json["message"] == "item_group_created"
        assert response.status_code == 201

        item_group = ItemGroup.query.order_by(ItemGroup.id.desc()).first()

        for key in base_item_group.keys():
            assert getattr(item_group, key) == base_item_group.get(key)

    # --------------------- DELETE ---------------------

    def test_delete_institution_with_non_registered_id(self, client):
        response = client.delete("/item_group/0")

        assert response.json["message"] == "item_group_not_found"
        assert response.status_code == 404

    def test_delete_item_group(self, client):
        response = client.delete("/item_group/1")

        assert response.json["message"] == "item_group_deleted"
        assert response.status_code == 200
