import pytest

from app.main import db
from app.test.seeders import create_base_seed_sanitary_district


@pytest.fixture(scope="module")
def seeded_database(client, database):
    """Seed database with sanitary district data"""
    return create_base_seed_sanitary_district(db)


@pytest.mark.usefixtures("seeded_database")
class TestSanitaryDistrictController:

    # --------------------- GET ---------------------

    def test_get_sanitary_districts(self, client):
        response = client.get("/sanitary_district")

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 2
        assert response.json["total_pages"] == 1

        assert response.json["items"][0]["id"] == 1
        assert response.json["items"][0]["name"] == "DISTRITO SANITÁRIO TESTE 1"
        assert response.json["items"][1]["id"] == 2
        assert response.json["items"][1]["name"] == "DISTRITO SANITÁRIO TESTE 2"

    def test_get_sanitary_district_by_name(self, client):
        response = client.get("/sanitary_district", query_string={"name": "Teste 1"})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 1
        assert response.json["total_pages"] == 1

        assert response.json["items"][0]["id"] == 1
        assert response.json["items"][0]["name"] == "DISTRITO SANITÁRIO TESTE 1"

    # --------------------- GET BY ID ---------------------

    def test_get_sanitary_district(self, client):
        response = client.get("/sanitary_district/1")

        assert response.status_code == 200
        assert response.json["id"] == 1
        assert response.json["name"] == "DISTRITO SANITÁRIO TESTE 1"

    def test_get_sanitary_district_with_invalid_id(self, client):
        response = client.get("/sanitary_district/0")

        assert response.status_code == 404
        assert response.json["message"] == "sanitary_district_not_found"

    # --------------------- PUT ---------------------

    def test_update_sanitary_district_with_invalid_id(
        self, client, base_sanitary_district
    ):
        response = client.put("/sanitary_district/0", json=base_sanitary_district)

        assert response.status_code == 404
        assert response.json["message"] == "sanitary_district_not_found"

    def test_update_sanitary_district_without_required_data(
        self, client, base_sanitary_district
    ):
        base_sanitary_district.pop("name", None)
        response = client.put("/sanitary_district/1", json=base_sanitary_district)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"

    def test_update_sanitary_district_with_registered_name(
        self, client, base_sanitary_district
    ):
        base_sanitary_district["name"] = "Distrito Sanitário Teste 2"
        response = client.put("/sanitary_district/1", json=base_sanitary_district)

        assert response.status_code == 409
        assert response.json["message"] == "name_in_use"

    def test_update_sanitary_district_with_empty_name(
        self, client, base_sanitary_district
    ):
        base_sanitary_district["name"] = ""
        response = client.put("/sanitary_district/1", json=base_sanitary_district)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert "name" in response.json["errors"].keys()

    def test_update_sanitary_district(self, client, base_sanitary_district):
        response = client.put("/sanitary_district/1", json=base_sanitary_district)

        assert response.status_code == 200
        assert response.json["message"] == "sanitary_district_updated"

    # --------------------- POST --------------------

    def test_create_sanitary_district_with_registered_name(
        self, client, base_sanitary_district
    ):
        response = client.post("/sanitary_district", json=base_sanitary_district)

        assert response.status_code == 409
        assert response.json["message"] == "name_in_use"

    def test_create_sanitary_district_without_required_data(
        self, client, base_sanitary_district
    ):
        base_sanitary_district.pop("name", None)
        response = client.post("/sanitary_district", json=base_sanitary_district)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"

    def test_create_sanitary_district_with_empty_name(
        self, client, base_sanitary_district
    ):
        base_sanitary_district["name"] = ""
        response = client.post("/sanitary_district", json=base_sanitary_district)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert "name" in response.json["errors"].keys()

    def test_create_sanitary_district(self, client, base_sanitary_district):
        base_sanitary_district["name"] = "DISTRITO SANITÁRIO TESTE 1"
        response = client.post("/sanitary_district", json=base_sanitary_district)

        assert response.status_code == 201
        assert response.json["message"] == "sanitary_district_created"

    # --------------------- DELETE ---------------------

    def test_delete_sanitary_district_with_invalid_id(self, client):
        response = client.delete("/sanitary_district/0")

        assert response.status_code == 404
        assert response.json["message"] == "sanitary_district_not_found"

    def test_delete_sanitary_district(self, client):
        response = client.delete("/sanitary_district/1")

        assert response.status_code == 200
        assert response.json["message"] == "sanitary_district_deleted"
