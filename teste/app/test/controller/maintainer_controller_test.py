import pytest

from app.main import db
from app.test.seeders import create_base_seed_maintainer


@pytest.fixture(scope="module")
def seeded_database(client, database):
    """Seed database with maintainer data"""
    return create_base_seed_maintainer(db)


@pytest.mark.usefixtures("seeded_database")
class TestmaintainerController:

    # --------------------- GET ---------------------
    def test_get_maintainers(self, client):
        response = client.get("/maintainer")
        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 2
        assert response.json["total_pages"] == 1
        assert response.json["items"][0]["corporate_name"] == "Hospital Central Teste 1"
        assert response.json["items"][0]["commercial_name"] == "Hospital Central Teste"
        assert response.json["items"][0]["cnpj"] == "02569021000158"
        assert response.json["items"][0]["regional_number"] == 11
        assert response.json["items"][0]["contact"]["phone"] == "8533165440"
        assert response.json["items"][0]["email"] == "maintaniner1@test.com"
        assert response.json["items"][1]["corporate_name"] == "Hospital Teste 1"
        assert response.json["items"][1]["commercial_name"] == "Hospital Teste"
        assert response.json["items"][1]["cnpj"] == "00623904000173"
        assert response.json["items"][1]["regional_number"] == 5
        assert response.json["items"][1]["contact"]["phone"] == "8532165498"
        assert response.json["items"][1]["email"] == "maintaniner2@test.com"

    def test_get_maintainers_by_page(self, client):
        response = client.get("/maintainer", query_string={"page": 2})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert len(response.json["items"]) == 0
        assert response.json["current_page"] == 2

    def test_get_maintainers_by_name(self, client):
        response = client.get(
            "/maintainer", query_string={"commercial_name": "Central"}
        )

        assert response.status_code == 200
        assert len(response.json) == 4
        assert len(response.json["items"]) == 1
        assert response.json["items"][0]["corporate_name"] == "Hospital Central Teste 1"
        assert response.json["items"][0]["commercial_name"] == "Hospital Central Teste"
        assert response.json["items"][0]["cnpj"] == "02569021000158"
        assert response.json["items"][0]["regional_number"] == 11
        assert response.json["items"][0]["contact"]["phone"] == "8533165440"
        assert response.json["items"][0]["email"] == "maintaniner1@test.com"
        assert response.json["current_page"] == 1

    # --------------------- UPDATE ---------------------

    def test_update_maintainer_with_invalid_cnpj(self, client, base_maintainer):
        base_maintainer["cnpj"] = "03569021000186"
        response = client.put("/maintainer/1", json=base_maintainer)

        assert response.status_code == 400
        assert "cnpj" in response.json["errors"].keys()

    def test_update_maintainer_with_registered_cnpj(self, client, base_maintainer):
        base_maintainer["cnpj"] = "00623904000173"
        response = client.put("/maintainer/1", json=base_maintainer)

        assert response.status_code == 409
        assert response.json["message"] == "cnpj_in_use"

    def test_update_maintainer_with_registered_email(self, client, base_maintainer):
        base_maintainer["email"] = "maintaniner2@test.com"

        response = client.put("/maintainer/1", json=base_maintainer)

        assert response.status_code == 409
        assert response.json["message"] == "email_in_use"

    def test_update_maintainer(self, client, base_maintainer):

        response = client.put("/maintainer/1", json=base_maintainer)
        assert response.status_code == 200
        assert response.json["message"] == "maintainer_updated"

    # --------------------- POST ---------------------

    @pytest.mark.parametrize(
        "key_popped",
        [
            "corporate_name",
            "commercial_name",
            "cnpj",
            "regional_number",
            "unit_type",
            "email",
        ],
        ids=[
            "without_corporate_name",
            "without_commercial_name",
            "without_cnpj",
            "without_regional_number",
            "without_unit_type",
            "without_email",
        ],
    )
    def test_register_maintainer_without_required_data(
        self, client, base_maintainer, key_popped
    ):
        base_maintainer.pop(key_popped, None)

        response = client.post("/maintainer", json=base_maintainer)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert key_popped in response.json["errors"].keys()

    def test_register_maintainer_with_invalid_cnpj(self, client, base_maintainer):
        base_maintainer["cnpj"] = "03569021000186"

        response = client.post("/maintainer", json=base_maintainer)

        assert response.status_code == 400
        assert "cnpj" in response.json["errors"].keys()

    def test_register_maintainer_with_registered_cnpj(self, client, base_maintainer):
        response = client.post("/maintainer", json=base_maintainer)

        assert response.status_code == 409
        assert response.json["message"] == "cnpj_in_use"

    def test_register_maintainer_with_registered_email(self, client, base_maintainer):
        base_maintainer["cnpj"] = "45305255000109"

        response = client.post("/maintainer", json=base_maintainer)

        assert response.status_code == 409
        assert response.json["message"] == "email_in_use"

    def test_register_maintainer(self, client, base_maintainer):

        base_maintainer["email"] = "maintaniner1@test.com"
        base_maintainer["cnpj"] = "45305255000109"

        response = client.post("/maintainer", json=base_maintainer)

        assert response.status_code == 201
        assert response.json["message"] == "maintainer_created"
