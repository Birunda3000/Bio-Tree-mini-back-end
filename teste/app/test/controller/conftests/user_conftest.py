import pytest


@pytest.fixture()
def base_user():
    """Base user data"""

    user = {"professional_id": 1, "login": "new_user@uece.br"}

    return user
