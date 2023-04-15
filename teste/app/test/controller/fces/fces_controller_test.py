import pytest

from app.main import db
from app.main.model import Fces
from app.test.seeders import (
    create_base_seed_fces,
    create_base_seed_maintainer,
    create_base_seed_professional,
    create_base_seed_sanitary_district,
)


@pytest.fixture(scope="module")
def seeded_database(client, database):
    """Seed database with fces data"""
    create_base_seed_professional(db)
    create_base_seed_maintainer(db)
    create_base_seed_sanitary_district(db)
    return create_base_seed_fces(db)


@pytest.mark.usefixtures("seeded_database")
class TestFcesController:
    # --------------------- GET ---------------------

    def test_get_fces(self, client):
        response = client.get("/fces")
        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 3
        assert response.json["total_pages"] == 1
        assert response.json["items"][0]["corporate_name"] == "Estabelecimento Teste 1"
        assert response.json["items"][0]["commercial_name"] == "Estabelecimento teste 1"
        assert response.json["items"][0]["cnes_code"] == 15866318
        assert response.json["items"][0]["person_type"] == "Jurídica"
        assert response.json["items"][0]["cnpj"] == "80280198000143"
        assert response.json["items"][0]["cpf"] == None
        assert response.json["items"][0]["email"] == "string@example.br"
        assert response.json["items"][1]["corporate_name"] == "Estabelecimento Teste 2"
        assert response.json["items"][1]["commercial_name"] == "Estabelecimento teste 2"
        assert response.json["items"][1]["cnes_code"] == 1598625
        assert response.json["items"][1]["person_type"] == "Física"
        assert response.json["items"][1]["cnpj"] == None
        assert response.json["items"][1]["cpf"] == "14525323892"
        assert response.json["items"][1]["email"] == "string2@example.br"

    def test_get_fces_by_page(self, client):
        response = client.get("/fces", query_string={"page": 2})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert len(response.json["items"]) == 0
        assert response.json["current_page"] == 2

    # --------------------- UPDATE ---------------------

    def test_update_fces_with_invalid_id(self, client, base_fces):
        response = client.put(
            "/fces/0",
            json=base_fces,
        )

        assert response.json["message"] == "fces_not_found"
        assert response.status_code == 404

    def test_update_fces_with_registered_corporate_name(self, client, base_fces):
        base_fces["corporate_name"] = "Estabelecimento Teste 2"

        response = client.put(
            "/fces/1",
            json=base_fces,
        )

        assert response.json["message"] == "corporate_name_in_use"
        assert response.status_code == 409

    def test_update_fces_with_registered_email(self, client, base_fces):
        base_fces["email"] = "string2@example.br"

        response = client.put(
            "/fces/1",
            json=base_fces,
        )

        assert response.json["message"] == "email_in_use"
        assert response.status_code == 409

    def test_update_fces(self, client, base_fces):
        base_fces.pop("cnes_code", None)
        base_fces.pop("person_type", None)
        base_fces.pop("cnpj", None)

        response = client.put(
            "/fces/1",
            json=base_fces,
        )

        assert response.json["message"] == "fces_updated"
        assert response.status_code == 200

        self._undo_fces_update_changes()

    # --------------------- CREATE ---------------------

    @pytest.mark.parametrize(
        "key_popped",
        [
            "maintainer_id",
            "professional_id",
            "corporate_name",
            "commercial_name",
            "cnes_code",
            "person_type",
            "establishment_code",
            "situation",
            "establishment_type",
            "establishment_subtype",
            "regulatory_registration_end_date",
            "payment_to_provider",
        ],
        ids=[
            "without_maintainer_id",
            "without_professional_id",
            "without_corporate_name",
            "without_commercial_name",
            "without_cnes_code",
            "without_person_type",
            "without_establishment_code",
            "without_situation",
            "without_establishment_type",
            "without_establishment_subtype",
            "without_regulatory_registration_end_date",
            "without_payment_to_provider",
        ],
    )
    def test_create_fces_without_required_data(self, client, base_fces, key_popped):
        base_fces.pop(key_popped, None)

        response = client.post(
            "/fces",
            json=base_fces,
        )

        assert response.json["message"] == "Input payload validation failed"
        assert response.status_code == 400
        assert key_popped in response.json["errors"].keys()

    @pytest.mark.parametrize(
        "key,new_value,expected_message",
        [
            # ("maintainer_id", 0, "maintainer_not_found"),
            ("professional_id", 0, "professional_not_found"),
        ],
        ids=[
            # "invalid_maintainer_id",
            "invalid_professional_id",
        ],
    )
    def test_create_fces_with_invalid_data(
        self,
        client,
        base_fces,
        key,
        new_value,
        expected_message,
    ):
        base_fces[key] = new_value

        response = client.post(
            "/fces",
            json=base_fces,
        )

        assert response.json["message"] == expected_message
        assert response.status_code == 404

    @pytest.mark.parametrize(
        "key,new_value",
        [
            ("person_type", "invalid_person_type"),
            (
                "situation",
                "invalid_situation",
            ),
            (
                "payment_to_provider",
                "invalid_payment_to_provider",
            ),
        ],
        ids=[
            "invalid_person_type",
            "invalid_situation",
            "invalid_payment_to_provider",
        ],
    )
    def test_create_fces_with_invalid_dto_data(self, client, base_fces, key, new_value):
        base_fces[key] = new_value

        response = client.post(
            "/fces",
            json=base_fces,
        )

        assert response.json["message"] == "Input payload validation failed"
        assert response.status_code == 400
        assert key in response.json["errors"].keys()

    def test_create_fces_with_invalid_cnpj(self, client, base_fces):
        base_fces["cnpj"] = "12345678910111"

        response = client.post(
            "/fces",
            json=base_fces,
        )

        assert response.json["message"] == "Input payload validation failed"
        assert response.status_code == 400

    def test_create_fces_with_invalid_cpf(self, client, base_fces):
        base_fces["person_type"] = "Física"
        base_fces.pop("cnpj", None)
        base_fces["cpf"] = "12345678910"

        response = client.post(
            "/fces",
            json=base_fces,
        )

        assert response.json["message"] == "Input payload validation failed"
        assert response.status_code == 400

    @pytest.mark.parametrize(
        "key,new_value,expected_message",
        [
            (
                "corporate_name",
                "Estabelecimento Teste 1",
                "corporate_name_in_use",
            ),
            ("cnes_code", 15866318, "cnes_code_in_use"),
        ],
        ids=[
            "registered_person_type",
            "registered_cnes_code",
        ],
    )
    def test_create_fces_with_registered_data(
        self, client, base_fces, key, new_value, expected_message
    ):
        base_fces[key] = new_value

        response = client.post(
            "/fces",
            json=base_fces,
        )

        assert response.json["message"] == expected_message
        assert response.status_code == 409

    def test_create_fces_with_registered_cnpj(self, client, base_fces):
        base_fces["cnpj"] = "80280198000143"

        response = client.post(
            "/fces",
            json=base_fces,
        )

        assert response.json["message"] == "cnpj_in_use"
        assert response.status_code == 409

    def test_create_fces_with_registered_cpf(self, client, base_fces):
        base_fces["person_type"] = "Física"
        base_fces.pop("cnpj", None)
        base_fces["cpf"] = "14525323892"

        response = client.post(
            "/fces",
            json=base_fces,
        )

        assert response.json["message"] == "cpf_in_use"
        assert response.status_code == 409

    def test_create_fces_with_registered_email(self, client, base_fces):
        base_fces["email"] = "string@example.br"

        response = client.post(
            "/fces",
            json=base_fces,
        )

        assert response.json["message"] == "email_in_use"
        assert response.status_code == 409

    def test_create_fces_with_cnpj_cpf_simultaneously(self, client, base_fces):
        base_fces["cpf"] = "24577128233"

        response = client.post(
            "/fces",
            json=base_fces,
        )

        assert response.json["message"] == "cnpj_cpf_sent_simultaneously"
        assert response.status_code == 400

    def test_create_fces(self, client, base_fces):
        response = client.post(
            "/fces",
            json=base_fces,
        )

        assert response.json["message"] == "fces_created"
        assert response.status_code == 201

    # --------------------- Helper functions  ---------------------

    def _undo_fces_update_changes(self) -> None:
        fces = Fces.query.get(1)

        fces.corporate_name = "Estabelecimento Teste 1"
        fces.cnes_code = 15866318
        fces.cnpj = "80280198000143"
        fces.email = "string@example.br"

        db.session.commit()
