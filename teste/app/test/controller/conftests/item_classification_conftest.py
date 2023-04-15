import pytest


@pytest.fixture()
def base_item_classification():
    """Base item classification"""

    item_classification = {"name": "item classification"}

    return item_classification
