import pytest

from app.main.model import Resource
from app.main.service import create_default_resources


@pytest.fixture(scope="module")
def seeded_database(database):
    """Seed database with default resources"""
    create_default_resources()


@pytest.mark.usefixtures("seeded_database")
class TestResourceController:
    def test_get_user(self, client):
        response = client.get("/resource")

        resources = [
            {"id": resource.id, "name": resource.name, "code": resource.code}
            for resource in Resource.query.all()
        ]

        assert len(response.json) == len(resources)
        assert response.status_code == 200
        assert response.json == resources
