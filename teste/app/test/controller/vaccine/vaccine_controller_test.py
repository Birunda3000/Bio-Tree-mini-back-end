import pytest

from app.main import db
from app.main.model import Vaccine
from app.test.seeders.vaccine import (
    create_base_seed_vaccine,
    create_base_seed_vaccine_laboratory,
)


@pytest.fixture(scope="module")
def seeded_database(database):
    """Seed database with vaccines"""
    create_base_seed_vaccine_laboratory(db)
    create_base_seed_vaccine(db)


@pytest.mark.usefixtures("seeded_database")
class TestVaccineController:

    # --------------------- GET  ---------------------
    def test_get_vaccines(self, client):
        response = client.get("/vaccine")

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 2
        assert response.json["total_pages"] == 1
        self._test_vaccine_teste_1_data(vaccine=response.json["items"][0])

    @pytest.mark.parametrize(
        "name",
        ["VACINA TESTE 1", "1"],
        ids=["complete_name", "incomplete_name"],
    )
    def test_get_vaccines_by_name(self, client, name):
        response = client.get("/vaccine", query_string={"name": name})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["total_items"] == 1
        self._test_vaccine_teste_1_data(vaccine=response.json["items"][0])

    # --------------------- GET BY NAME ---------------------
    def test_get_vaccine_by_name(self, client):
        response = client.get("/vaccine/vacina")

        assert response.status_code == 200
        assert len(response.json) == 2
        self._test_vaccine_teste_1_data(vaccine=response.json[0])

    def test_get_vaccine_by_short_name(self, client):
        response = client.get("/vaccine/va")

        assert response.status_code == 400
        assert "vaccine_name" in response.json["errors"].keys()

    def test_get_vaccine_by_exact_name(self, client):
        response = client.get("/vaccine/vacina%20teste%201")
        assert response.status_code == 200
        assert len(response.json) == 1
        self._test_vaccine_teste_1_data(vaccine=response.json[0])

    # --------------------- GET BY ID ---------------------
    def test_get_vaccine_by_id(self, client):
        response = client.get("/vaccine/1")

        assert response.status_code == 200
        assert response.json["id"] == 1
        assert response.json["name"] == "VACINA TESTE 1"
        assert response.json["pni_code"] == "00123"
        assert response.json["belongs_to_vaccine_card"] == True
        assert response.json["current"] == True
        assert response.json["export_to_esus"] == False
        assert response.json["controls_vaccine_batch"] == True
        assert response.json["oblige_establishment"] == False
        assert response.json["laboratories"] == [
            {
                "id": 1,
                "name": "LABORATORIO TESTE 1",
                "pni_code": "COD001",
                "cnpj": "88649316000150",
            },
            {
                "id": 2,
                "name": "LABORATORIO TESTE 2",
                "pni_code": "COD002",
                "cnpj": "35490474000143",
            },
        ]

    def test_get_vaccine_by_invalid_id(self, client):
        response = client.get("/vaccine/0")

        assert response.status_code == 404
        assert response.json["message"] == "vaccine_not_found"

    # --------------------- POST ---------------------
    @pytest.mark.parametrize(
        "key_popped",
        [
            "name",
            "laboratory_ids",
            "pni_code",
            "belongs_to_vaccine_card",
            "current",
            "export_to_esus",
            "controls_vaccine_batch",
            "oblige_establishment",
        ],
        ids=[
            "without_name",
            "without_laboratory_ids",
            "without_pni_code_field",
            "without_belongs_to_vaccine_card_field",
            "without_current_field",
            "without_export_to_esus_field",
            "without_controls_vaccine_batch_field",
            "without_oblige_establishment_field",
        ],
    )
    def test_create_vaccine_without_required_data(
        self, client, base_vaccine, key_popped
    ):
        base_vaccine.pop(key_popped, None)
        response = client.post("/vaccine", json=base_vaccine)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert key_popped in response.json["errors"].keys()

    def test_create_vaccine_without_laboratories(
        self,
        client,
        base_vaccine,
    ):
        base_vaccine["laboratory_ids"] = []
        response = client.post("/vaccine", json=base_vaccine)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert "laboratory_ids" in response.json["errors"].keys()

    def test_create_vaccine_with_non_registered_laboratory_id(
        self, client, base_vaccine
    ):
        base_vaccine["laboratory_ids"] = [0, 1]
        response = client.post("/vaccine", json=base_vaccine)

        assert response.status_code == 404
        assert response.json["message"] == "vaccine_laboratory_not_found"

    def test_create_vaccine_with_registered_name(self, client, base_vaccine):
        base_vaccine["name"] = "vacina teste 1"
        response = client.post("/vaccine", json=base_vaccine)

        assert response.status_code == 409
        assert response.json["message"] == "vaccine_already_exists"

    def test_create_vaccine_with_empty_name(self, client, base_vaccine):
        base_vaccine["name"] = ""
        response = client.post("/vaccine", json=base_vaccine)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert "name" in response.json["errors"].keys()

    def test_create_vaccine(self, client, base_vaccine):
        base_vaccine["name"] = "vacina teste 3"

        response = client.post("/vaccine", json=base_vaccine)

        assert response.status_code == 201
        assert response.json["message"] == "vaccine_created"

        self._test_vaccine_vaccine_name_saved_in_uppercase(id=3)

    # --------------------- PUT ---------------------
    @pytest.mark.parametrize(
        "key_popped",
        [
            "name",
            "laboratory_ids",
            "pni_code",
            "belongs_to_vaccine_card",
            "current",
            "export_to_esus",
            "controls_vaccine_batch",
            "oblige_establishment",
        ],
        ids=[
            "without_name",
            "without_laboratory_ids",
            "without_pni_code_field",
            "without_belongs_to_vaccine_card_field",
            "without_current_field",
            "without_export_to_esus_field",
            "without_controls_vaccine_batch_field",
            "without_oblige_establishment_field",
        ],
    )
    def test_update_vaccine_without_required_data(
        self, client, base_vaccine, key_popped
    ):
        base_vaccine.pop(key_popped, None)
        response = client.put("/vaccine/1", json=base_vaccine)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert key_popped in response.json["errors"].keys()

    def test_update_vaccine_with_invalid_id(self, client, base_vaccine):
        response = client.put("/vaccine/0", json=base_vaccine)

        assert response.status_code == 404
        assert response.json["message"] == "vaccine_not_found"

    def test_update_vaccine_with_invalid_data(self, client, base_vaccine):
        base_vaccine["laboratory_ids"] = []
        response = client.put("/vaccine/1", json=base_vaccine)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert "laboratory_ids" in response.json["errors"].keys()

    def test_update_vaccine_with_non_registered_laboratory_id(
        self, client, base_vaccine
    ):
        base_vaccine["laboratory_ids"] = [0]
        response = client.put("/vaccine/1", json=base_vaccine)

        assert response.status_code == 404
        assert response.json["message"] == "vaccine_laboratory_not_found"

    def test_update_vaccine_with_registered_name(self, client, base_vaccine):
        base_vaccine["name"] = "vacina teste 2"
        response = client.put("/vaccine/1", json=base_vaccine)

        assert response.status_code == 409
        assert response.json["message"] == "vaccine_already_exists"

    def test_update_vaccine(self, client, base_vaccine):
        base_vaccine["name"] = "vacina teste 1"

        response = client.put("/vaccine/1", json=base_vaccine)

        assert response.status_code == 200
        assert response.json["message"] == "vaccine_updated"

        self._test_vaccine_vaccine_name_saved_in_uppercase(id=1)

    # --------------------- Helper Functions ---------------------
    def _test_vaccine_teste_1_data(self, vaccine: dict[str, any]) -> None:

        assert vaccine["id"] == 1
        assert vaccine["name"] == "VACINA TESTE 1"

    def _test_vaccine_vaccine_name_saved_in_uppercase(self, id: int) -> None:
        vaccine = Vaccine.query.get(id)

        assert vaccine.name == f"VACINA TESTE {id}"
