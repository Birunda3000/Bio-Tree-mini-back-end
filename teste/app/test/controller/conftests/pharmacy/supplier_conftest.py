import pytest


@pytest.fixture()
def base_supplier():
    supplier = {"name": "SUPPLIER"}

    return supplier


@pytest.fixture()
def base_supplier_as_natural_person():
    supplier = {"name": "SUPPLIER NATURAL PERSON", "cpf": "34378612046"}

    return supplier


@pytest.fixture()
def base_supplier_as_legal_person():
    supplier = {"name": "SUPPLIER LEGAL PERSON", "cnpj": "42412145957240"}

    return supplier
