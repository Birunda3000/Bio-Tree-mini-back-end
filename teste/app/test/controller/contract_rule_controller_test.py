import os

import pytest
from pytest_mock.plugin import MockerFixture

from app.main import db
from app.main.model import ContractRule
from app.test.seeders import create_base_seed_contract_rule

CONTRACT_RULES_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    "resources",
    "contract_rules",
)


@pytest.fixture(scope="module")
def seeded_database(client, database):
    """Seed database with contract rule data"""
    return create_base_seed_contract_rule(db)


@pytest.mark.usefixtures("seeded_database")
class TestContractRuleController:

    # --------------------- GET ---------------------

    def test_get_contract_rules(self, client):
        response = client.get("/contract_rule")

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 2
        assert response.json["total_pages"] == 1
        self._test_contract_rule_with_id_1_data(item=response.json["items"][0])

    @pytest.mark.parametrize(
        "parameter, value",
        [
            ("description", "regra contratual teste 1"),
            ("description", "1"),
        ],
        ids=[
            "complete_description",
            "incomplete_description",
        ],
    )
    def test_get_contract_rules_by_parameters(self, client, parameter, value):
        response = client.get("/contract_rule", query_string={parameter: value})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 1
        assert response.json["total_pages"] == 1
        self._test_contract_rule_with_id_1_data(item=response.json["items"][0])

    # --------------------- GET BY ID  ---------------------

    def test_get_contract_rule_by_id(self, client):
        response = client.get("/contract_rule/1")

        assert response.status_code == 200
        assert len(response.json) == 5
        self._test_contract_rule_with_id_1_data(item=response.json)

    def test_get_contract_rule_by_invalid_id(self, client):
        response = client.get("/contract_rule/0")

        assert response.status_code == 404
        assert response.json["message"] == "contract_rule_not_found"

    # --------------------- PUT ---------------------

    def test_update_contract_rule_with_invalid_id(self, client, base_contract_rule):
        response = client.put("/contract_rule/0", json=base_contract_rule)

        assert response.status_code == 404
        assert response.json["message"] == "contract_rule_not_found"

    @pytest.mark.parametrize(
        "key, value",
        [("type", "invalid_type")],
        ids=["with_invalid_type"],
    )
    def test_update_contract_rule_with_invalid_data(
        self, client, base_contract_rule, key, value
    ):
        base_contract_rule[key] = value
        response = client.put("/contract_rule/1", json=base_contract_rule)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert key in response.json["errors"].keys()

    @pytest.mark.parametrize(
        "key_popped",
        [
            "code",
            "description",
            "ordinance",
            "type",
        ],
        ids=[
            "without_code",
            "without_description",
            "without_ordinance",
            "without_type",
        ],
    )
    def test_update_contract_rule_without_required_data(
        self, client, base_contract_rule, key_popped
    ):
        del base_contract_rule[key_popped]
        response = client.put("/contract_rule/1", json=base_contract_rule)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert key_popped in response.json["errors"].keys()

    @pytest.mark.parametrize(
        "key, value, message",
        [
            ("code", "00.02", "code_in_use"),
        ],
        ids=[
            "registered_code",
        ],
    )
    def test_update_contract_rule_with_registered_data(
        self, client, base_contract_rule, key, value, message
    ):
        base_contract_rule[key] = value
        response = client.put("/contract_rule/1", json=base_contract_rule)

        assert response.status_code == 409
        assert response.json["message"] == message

    def test_update_contract_rule(self, client, base_contract_rule):
        response = client.put("/contract_rule/1", json=base_contract_rule)

        assert response.status_code == 200
        assert response.json["message"] == "contract_rule_updated"

        self._undo_contract_rule_update_changes()

    def test_update_contract_rule_ended_by_00_and_with_no_type(
        self, client, base_contract_rule
    ):
        base_contract_rule["code"] = "00.00"
        del base_contract_rule["type"]
        response = client.put("/contract_rule/1", json=base_contract_rule)

        assert response.status_code == 200
        assert response.json["message"] == "contract_rule_updated"

        self._undo_contract_rule_update_changes()

    # --------------------- POST ---------------------

    @pytest.mark.parametrize(
        "key, value",
        [("type", "invalid_type")],
        ids=["with_invalid_type"],
    )
    def test_create_contract_rule_with_invalid_data(
        self, client, base_contract_rule, key, value
    ):
        base_contract_rule[key] = value
        response = client.post("/contract_rule", json=base_contract_rule)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert key in response.json["errors"].keys()

    @pytest.mark.parametrize(
        "key_popped",
        [
            "code",
            "description",
            "ordinance",
            "type",
        ],
        ids=[
            "without_code",
            "without_description",
            "without_ordinance",
            "without_type",
        ],
    )
    def test_create_contract_rule_without_required_data(
        self, client, base_contract_rule, key_popped
    ):
        del base_contract_rule[key_popped]
        response = client.post("/contract_rule", json=base_contract_rule)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert key_popped in response.json["errors"].keys()

    @pytest.mark.parametrize(
        "key, value, message",
        [
            ("code", "00.02", "code_in_use"),
        ],
        ids=[
            "registered_code",
        ],
    )
    def test_create_contract_rule_with_registered_data(
        self, client, base_contract_rule, key, value, message
    ):
        base_contract_rule[key] = value
        response = client.post("/contract_rule", json=base_contract_rule)

        assert response.status_code == 409
        assert response.json["message"] == message

    def test_create_contract_rule(self, client, base_contract_rule):
        response = client.post("/contract_rule", json=base_contract_rule)

        assert response.status_code == 201
        assert response.json["message"] == "contract_rule_created"

        self._delete_contract_rules_from_db(ids=[3])

    def test_create_contract_rule_ended_by_00_and_with_no_type(
        self, client, base_contract_rule
    ):
        base_contract_rule["code"] = "01.00"
        del base_contract_rule["type"]
        response = client.post("/contract_rule", json=base_contract_rule)

        assert response.status_code == 201
        assert response.json["message"] == "contract_rule_created"

        self._delete_contract_rules_from_db(ids=[3])

    # --------------------- POST - IMPORT ---------------------

    def test_import_contract_rules_from_url_returning_invalid_code(
        self, client, mocker, base_contract_rule_import
    ):
        mock_requests = mocker.patch("requests.get")
        mock_requests.return_value.status_code = 404

        response = client.post("/contract_rule/import", json=base_contract_rule_import)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert "url" in response.json["errors"].keys()

    @pytest.mark.parametrize(
        "url",
        [
            "teste.com",
            "https://teste",
        ],
        ids=[
            "withou_https",
            "withou_dot_com",
        ],
    )
    def test_import_contract_rules_from_invalid_url(
        self, client, base_contract_rule_import, url
    ):
        base_contract_rule_import["url"] = url
        response = client.post("/contract_rule/import", json=base_contract_rule_import)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert "url" in response.json["errors"].keys()

    @pytest.mark.parametrize(
        "file_path",
        [
            "contract_rules_with_one_table.html",
            "contract_rules_with_multiple_tables.html",
            "contract_rules_with_strikethrough_lines.html",
        ],
        ids=[
            "with_one_table",
            "with_mutiple_tables",
            "with_strikethrough_lines",
        ],
    )
    def test_import_contract_rules(
        self, client, mocker, base_contract_rule_import, file_path
    ):
        self._mock_requests_get(file_path=file_path, status_code=200, mocker=mocker)

        response = client.post("/contract_rule/import", json=base_contract_rule_import)

        assert response.status_code == 201
        assert response.json["message"] == "contract_rules_imported"

        contract_rules = ContractRule.query.order_by(ContractRule.id).all()

        assert len(contract_rules) == 4
        self._check_contract_rule_data(
            contract_rule=contract_rules[2],
            data={
                "id": 3,
                "code": "09.00",
                "description": "TABELA DE ADESÃO A PROGRAMA/PROJETO DE SAÚDE",
                "type": None,
            },
        )
        self._check_contract_rule_data(
            contract_rule=contract_rules[3],
            data={
                "id": 4,
                "code": "09.01",
                "description": "ADESÃO DO MUNICIPIO AO PROGRAMA DE HOSPITAL DE PEQUENO PORTE",
                "type": "CENTRALIZADA",
            },
        )

        self._delete_contract_rules_from_db(ids=[3, 4])

    def test_upsert_import_contract_rules(
        self, client, mocker, base_contract_rule_import
    ):
        self._mock_requests_get(
            file_path="contract_rules_added_with_different_values.html",
            status_code=200,
            mocker=mocker,
        )

        response = client.post("/contract_rule/import", json=base_contract_rule_import)

        assert response.status_code == 201
        assert response.json["message"] == "contract_rules_imported"

        contract_rules = ContractRule.query.order_by(ContractRule.id).all()

        assert len(contract_rules) == 2
        self._check_contract_rule_data(
            contract_rule=contract_rules[0],
            data={
                "id": 1,
                "code": "00.01",
                "description": "regra contratual teste 1 - atualizada",
                "type": "DESCENTRALIZADA",
            },
        )
        self._check_contract_rule_data(
            contract_rule=contract_rules[1],
            data={
                "id": 2,
                "code": "00.02",
                "description": "regra contratual teste 2 - atualizada",
                "type": "CENTRALIZADA",
            },
        )

        self._delete_contract_rules_from_db(ids=[3, 4])

    # --------------------- DELETE ---------------------

    def test_delete_contract_rule_with_non_registered_id(self, client):
        response = client.delete("/contract_rule/0")

        assert response.status_code == 404
        assert response.json["message"] == "contract_rule_not_found"

    def test_delete_contract_rule(self, client):
        response = client.delete("/contract_rule/1")

        assert response.status_code == 200
        assert response.json["message"] == "contract_rule_deleted"

    # --------------------- Helper functions  ---------------------
    def _test_contract_rule_with_id_1_data(self, item: dict[str, any]) -> None:
        assert item["id"] == 1
        assert item["code"] == "00.01"
        assert item["description"] == "regra contratual teste 1"
        assert item["ordinance"] == "teste"
        assert item["type"] == "CENTRALIZADA"

    def _undo_contract_rule_update_changes(self):
        contract_rule = ContractRule.query.get(1)

        contract_rule.code = "00.01"
        contract_rule.description = "regra contratual teste 1"
        contract_rule.ordinance = "teste"
        contract_rule.type = "CENTRALIZADA"

        db.session.add(contract_rule)
        db.session.commit()

    def _delete_contract_rules_from_db(self, ids: list[int]) -> None:
        ContractRule.query.filter(ContractRule.id.in_(ids)).delete()
        db.session.commit()

    def _mock_requests_get(
        self, file_path: str, status_code: int, mocker: MockerFixture
    ) -> None:
        with open(
            os.path.join(CONTRACT_RULES_DIR, file_path), encoding="utf-8"
        ) as teste:
            mock_requests = mocker.patch("requests.get")
            mock_requests.return_value.status_code = status_code
            mock_requests.return_value.text = teste.read()

    def _check_contract_rule_data(
        self, contract_rule: ContractRule, data: dict[str, any]
    ) -> None:
        assert contract_rule.id == data["id"]
        assert contract_rule.code == data["code"]
        assert contract_rule.description == data["description"]
        assert contract_rule.ordinance == "teste"
        assert contract_rule.type == data["type"]
