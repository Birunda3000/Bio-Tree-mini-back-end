import pytest

from app.main.model import Queue
from app.main.service import create_default_queues


@pytest.fixture(scope="module")
def seeded_database(database):
    """Seed database with default queues"""
    return create_default_queues()


@pytest.mark.usefixtures("seeded_database")
class TestQueueController:
    def test_get_queues(self, client):
        response = client.get("/queue")

        queues = [
            {
                "id": queue.id,
                "name": queue.name,
            }
            for queue in Queue.query.all()
        ]

        assert response.status_code == 200
        assert response.json == queues
