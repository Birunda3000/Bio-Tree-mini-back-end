import pytest


@pytest.fixture()
def base_protocol():
    """Base protocol data"""
    protocol = {"name": "teste", "protocol_type": "Diagnóstico"}

    return protocol
