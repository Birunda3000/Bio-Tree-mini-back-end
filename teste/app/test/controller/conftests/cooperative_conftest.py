import pytest


@pytest.fixture()
def base_cooperative():
    """Base cooperative"""

    cooperative = {"name": "Cooperativa teste 3", "cbo": "CBO3"}

    return cooperative
