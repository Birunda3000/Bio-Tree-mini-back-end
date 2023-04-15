import pytest


@pytest.fixture()
def base_room():
    """Base room"""

    room = {"name": "Sala Teste 1"}

    return room
