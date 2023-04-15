import pytest

from app.main import db
from app.main.model import VaccineLaboratory
from app.test.seeders import create_base_seed_vaccine_laboratory


@pytest.fixture(scope="module")
def seeded_database(client, database):
    """Seed database with vacine laboratory data"""
    create_base_seed_vaccine_laboratory(db)


@pytest.mark.usefixtures("seeded_database")
class TestVacineLaboratoryController:

    # --------------------- GET ---------------------
    def test_get_vaccine_laboratories(self, client):
        response = client.get("/vaccine/laboratory")

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 2
        assert response.json["total_pages"] == 1
        self._test_vaccine_laboratory_item_1_data(data=response.json["items"][0])

    @pytest.mark.parametrize(
        "name",
        ["laboratorio teste 1", "1"],
        ids=["complete_name", "incomplete_name"],
    )
    def test_get_vaccine_laboratories_by_name(self, client, name):
        response = client.get("/vaccine/laboratory", query_string={"name": name})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["total_items"] == 1
        self._test_vaccine_laboratory_item_1_data(data=response.json["items"][0])

    # --------------------- GET BY ID ---------------------
    def test_get_vaccine_laboratory(self, client):
        response = client.get("/vaccine/laboratory/1")

        assert response.status_code == 200
        self._test_vaccine_laboratory_item_1_data(data=response.json)

    def test_get_vaccine_laboratory_with_invalid_id(self, client):
        response = client.get("/vaccine/laboratory/0")

        assert response.status_code == 404
        assert response.json["message"] == "vaccine_laboratory_not_found"

    # --------------------- POST ---------------------
    @pytest.mark.parametrize(
        "key_popped",
        ["name", "pni_code"],
        ids=["without_name", "without_pni_code"],
    )
    def test_create_vaccine_laboratory_without_required_data(
        self, client, base_vaccine_laboratory, key_popped
    ):
        del base_vaccine_laboratory[key_popped]
        response = client.post("/vaccine/laboratory", json=base_vaccine_laboratory)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert key_popped in response.json["errors"].keys()

    @pytest.mark.parametrize(
        "key,value,message",
        [
            ("name", "laboratorio teste 1", "name_in_use"),
            ("pni_code", "COD001", "pni_code_in_use"),
            ("cnpj", "88649316000150", "cnpj_in_use"),
        ],
        ids=["name", "pni_code", "cnpj"],
    )
    def test_create_vaccine_laboratory_with_registered_data(
        self, client, base_vaccine_laboratory, key, value, message
    ):
        base_vaccine_laboratory[key] = value
        response = client.post("/vaccine/laboratory", json=base_vaccine_laboratory)

        assert response.status_code == 409
        assert response.json["message"] == message

    def test_create_vaccine_laboratory_with_invalid_cnpj(
        self, client, base_vaccine_laboratory
    ):
        base_vaccine_laboratory["cnpj"] = "12345678910112"
        response = client.post("/vaccine/laboratory", json=base_vaccine_laboratory)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert "cnpj" in response.json["errors"].keys()

    def test_create_vaccine_laboratory_with_empty_name(
        self, client, base_vaccine_laboratory
    ):
        base_vaccine_laboratory["name"] = ""
        response = client.post("/vaccine/laboratory", json=base_vaccine_laboratory)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert "name" in response.json["errors"].keys()

    def test_create_vaccine_laboratory(self, client, base_vaccine_laboratory):
        base_vaccine_laboratory["name"] = "laboratorio teste 3"

        response = client.post("/vaccine/laboratory", json=base_vaccine_laboratory)

        assert response.status_code == 201
        assert response.json["message"] == "vaccine_laboratory_created"

        self._test_vaccine_laboratory_saved_in_lowercase(id=3)

    # --------------------- PUT ---------------------

    @pytest.mark.parametrize(
        "key_popped",
        ["name", "pni_code"],
        ids=["without_name", "without_pni_code"],
    )
    def test_update_vaccine_laboratory_without_required_data(
        self, client, base_vaccine_laboratory, key_popped
    ):
        del base_vaccine_laboratory[key_popped]
        response = client.put("/vaccine/laboratory/1", json=base_vaccine_laboratory)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert key_popped in response.json["errors"].keys()

    def test_update_vaccine_laboratory_with_invalid_id(
        self, client, base_vaccine_laboratory
    ):
        response = client.put("/vaccine/laboratory/0", json=base_vaccine_laboratory)

        assert response.status_code == 404
        assert response.json["message"] == "vaccine_laboratory_not_found"

    @pytest.mark.parametrize(
        "key,value,message",
        [
            ("name", "laboratorio teste 1", "name_in_use"),
            ("pni_code", "COD000", "pni_code_in_use"),
            ("cnpj", "60972319000100", "cnpj_in_use"),
        ],
        ids=["name", "pni_code", "cnpj"],
    )
    def test_update_vaccine_laboratory_with_registered_data(
        self, client, base_vaccine_laboratory, key, value, message
    ):
        base_vaccine_laboratory[key] = value
        if key is not "name":
            base_vaccine_laboratory["name"] = "laboratorio teste 0"
        if key is not "cnpj":
            base_vaccine_laboratory["cnpj"] = "83682479000110"
        if key is not "pni_code":
            base_vaccine_laboratory["pni_code"] = "COD999"

        response = client.put("/vaccine/laboratory/2", json=base_vaccine_laboratory)

        assert response.status_code == 409
        assert response.json["message"] == message

    def test_update_vaccine_laboratory_with_invalid_cnpj(
        self, client, base_vaccine_laboratory
    ):
        base_vaccine_laboratory["cnpj"] = "12345678910112"
        response = client.put("/vaccine/laboratory/1", json=base_vaccine_laboratory)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert "cnpj" in response.json["errors"].keys()

    def test_update_vaccine_laboratory_with_empty_name(
        self, client, base_vaccine_laboratory
    ):
        base_vaccine_laboratory["name"] = ""
        response = client.put("/vaccine/laboratory/1", json=base_vaccine_laboratory)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert "name" in response.json["errors"].keys()

    def test_update_vaccine_laboratory(self, client, base_vaccine_laboratory):
        base_vaccine_laboratory["cnpj"] = "45305255000109"
        base_vaccine_laboratory["name"] = "laboratorio teste 1"
        base_vaccine_laboratory["pni_code"] = "COD009"

        response = client.put("/vaccine/laboratory/1", json=base_vaccine_laboratory)

        assert response.json["message"] == "vaccine_laboratory_updated"

        self._test_vaccine_laboratory_saved_in_lowercase(id=1)

    # --------------------- Helper Functions ---------------------
    def _test_vaccine_laboratory_saved_in_lowercase(self, id: int) -> None:
        vaccine_laboratory = VaccineLaboratory.query.get(id)

        assert vaccine_laboratory.name == f"LABORATORIO TESTE {id}"

    def _test_vaccine_laboratory_item_1_data(self, data: dict[str, any]) -> None:
        assert data["id"] == 1
        assert data["name"] == "LABORATORIO TESTE 1"
        assert data["pni_code"] == "COD001"
        assert data["cnpj"] == "88649316000150"
