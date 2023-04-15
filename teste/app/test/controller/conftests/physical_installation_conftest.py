import pytest


@pytest.fixture()
def base_physical_installation_type():
    """Base physical installation type"""

    physical_installation_type = {"name": "TIPO DE INSTALAÇÃO FÍSICA TESTE 3"}

    return physical_installation_type


@pytest.fixture()
def base_physical_installation_subtype():
    """Base physical installation subtype"""

    physical_installation_subtype = {
        "name": "SUBTIPO DE INSTALAÇÃO FÍSICA TESTE 3",
    }

    return physical_installation_subtype
