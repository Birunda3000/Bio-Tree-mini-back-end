import pytest

from app.main import db
from app.test.seeders import create_base_seed_item_classification


@pytest.fixture(scope="module")
def seeded_database(client, database):
    """Seed database with prescription data"""

    return create_base_seed_item_classification(db)


@pytest.mark.usefixtures("seeded_database")
class TestItemClassificationController:

    # --------------------- GET ITEM CLASSIFICATIONS ---------------------

    def test_get_item_classifications(self, client):
        response = client.get("/item_classification")

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 3
        assert response.json["total_pages"] == 1
        assert response.json["items"][0]["id"] == 1
        assert response.json["items"][0]["name"] == "ITEM CLASSIFICATION ONE"
        assert response.json["items"][1]["id"] == 2
        assert response.json["items"][1]["name"] == "ITEM CLASSIFICATION TWO"
        assert response.json["items"][2]["id"] == 3
        assert response.json["items"][2]["name"] == "ITEM CLASSIFICATION THREE"

    def test_get_item_classifications_by_name(self, client):
        response = client.get("/item_classification", query_string={"name": "One"})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 1
        assert response.json["total_pages"] == 1
        assert response.json["items"][0]["id"] == 1
        assert response.json["items"][0]["name"] == "ITEM CLASSIFICATION ONE"

    # --------------------- GET ITEM CLASSIFICATION  ---------------------

    def test_get_item_classification(self, client):
        response = client.get("/item_classification/1")

        assert response.status_code == 200
        assert len(response.json) == 2
        assert response.json["id"] == 1
        assert response.json["name"] == "ITEM CLASSIFICATION ONE"

    def test_get_item_classification_by_invalid_id(self, client):
        response = client.get("/item_classification/0")

        assert response.status_code == 404
        assert response.json["message"] == "item_classification_not_found"

    # --------------------- UPDATE ITEM CLASSIFICATION ---------------------

    def test_update_item_classification_with_invalid_data(
        self, client, base_item_classification
    ):
        base_item_classification["name"] = 0
        response = client.put("/item_classification/1", json=base_item_classification)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"

    def test_update_item_classification_by_invalid_id(
        self, client, base_item_classification
    ):
        response = client.put("/item_classification/0", json=base_item_classification)

        assert response.status_code == 404
        assert response.json["message"] == "item_classification_not_found"

    def test_update_item_classification_with_registered_name(
        self, client, base_item_classification
    ):
        base_item_classification["name"] = "item classification two"
        response = client.put("/item_classification/1", json=base_item_classification)

        assert response.status_code == 409
        assert response.json["message"] == "name_in_use"

    def test_update_item_classification(self, client, base_item_classification):
        response = client.put("/item_classification/1", json=base_item_classification)

        assert response.status_code == 200
        assert response.json["message"] == "item_classification_updated"

    # --------------------- CREATE ITEM CLASSIFICATION ---------------------

    def test_create_item_classification_with_invalid_data(
        self, client, base_item_classification
    ):
        base_item_classification["name"] = 0
        response = client.post("/item_classification", json=base_item_classification)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"

    def test_create_item_classification_with_registered_name(
        self, client, base_item_classification
    ):
        response = client.post("/item_classification", json=base_item_classification)

        assert response.status_code == 409
        assert response.json["message"] == "name_in_use"

    def test_create_item_classification(self, client, base_item_classification):
        base_item_classification["name"] = "item classification one"
        response = client.post("/item_classification", json=base_item_classification)

        assert response.status_code == 201
        assert response.json["message"] == "item_classification_created"

    # --------------------- DELETE ITEM CLASSIFICATION ---------------------

    def test_delete_prescription_with_non_registered_id(self, client):
        response = client.delete("/item_classification/0")

        assert response.status_code == 404
        assert response.json["message"] == "item_classification_not_found"

    def test_delete_item_classification(self, client):
        response = client.delete("/item_classification/1")

        assert response.status_code == 200
        assert response.json["message"] == "item_classification_deleted"
