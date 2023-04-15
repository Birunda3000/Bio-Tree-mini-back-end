import pytest

from app.main import db
from app.test.seeders import create_base_seed_leavings


@pytest.fixture(scope="module")
def seeded_database(client, database):
    """Seed database with commission type data"""
    create_base_seed_leavings(db)


@pytest.mark.usefixtures("seeded_database")
class TestLeavingsController:

    # --------------------- GET  ---------------------
    def test_get_leavings(self, client):
        response = client.get("/leavings")

        assert response.status_code == 200
        assert len(response.json) == 5
        assert response.json[0]["id"] == 1
        assert response.json[0]["name"] == "RESÍDUOS BIOLÓGICOS"
        assert response.json[1]["id"] == 2
        assert response.json[1]["name"] == "RESÍDUOS QUÍMICOS"

    # ------------------ GET BY ID -------------------

    def test_get_cid_10_by_exact_name(self, client):
        response = client.get("/leavings/4")
        assert response.status_code == 200
        assert len(response.json) == 2
        assert response.json["id"] == 4
        assert response.json["name"] == "RESÍDUOS COMUNS"
