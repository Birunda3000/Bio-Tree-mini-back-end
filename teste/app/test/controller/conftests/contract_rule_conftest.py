import pytest


@pytest.fixture()
def base_contract_rule():
    """Base contract rule data"""
    contract_rule = {
        "code": "00.03",
        "description": "Regra contratual teste 3",
        "ordinance": "teste",
        "type": "CENTRALIZADA",
    }

    return contract_rule


@pytest.fixture()
def base_contract_rule_import():
    """Base contract rule import data"""
    contract_rule = {"url": "http://teste.com", "ordinance": "teste"}

    return contract_rule
