import pytest


@pytest.fixture()
def base_item_group():
    item_group = {
        "name": "ITEM GROUP",
    }

    return item_group
