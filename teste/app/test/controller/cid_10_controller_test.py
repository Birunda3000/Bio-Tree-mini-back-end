import pytest

from app.main import db
from app.test.seeders import create_base_seed_cid_10


@pytest.fixture(scope="module")
def seeded_database(client, database):
    """Seed database with cid 10 data"""
    create_base_seed_cid_10(db)


@pytest.mark.usefixtures("seeded_database")
class TestCid10Controller:

    # --------------------- GET CID 10 BY CODE ---------------------
    def test_get_cid_10_by_code(self, client):
        response = client.get("/cid10/S")

        assert response.status_code == 200
        assert len(response.json) == 2
        assert response.json[0]["id"] == 1
        assert response.json[0]["code"] == "S02"
        assert response.json[0]["category"] == 19
        assert response.json[1]["id"] == 2
        assert response.json[1]["code"] == "S022"
        assert response.json[1]["category"] == 19

    def test_get_cid_10_by_exact_name(self, client):
        response = client.get("/cid10/S022")
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]["id"] == 2
        assert response.json[0]["code"] == "S022"
        assert response.json[0]["category"] == 19
