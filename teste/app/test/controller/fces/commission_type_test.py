import pytest

from app.main import db
from app.test.seeders import create_base_seed_commission_type


@pytest.fixture(scope="module")
def seeded_database(client, database):
    """Seed database with commission type data"""
    create_base_seed_commission_type(db)


@pytest.mark.usefixtures("seeded_database")
class TestCommissionTypeController:

    # --------------------- GET  ---------------------
    def test_get_commission_types(self, client):
        response = client.get("/commission_types")

        assert response.status_code == 200
        assert len(response.json) == 15
        assert response.json[0]["id"] == 1
        assert response.json[0]["name"] == "ÉTICA MÉDICA"
        assert response.json[1]["id"] == 2
        assert response.json[1]["name"] == "ÉTICA DE ENFERMAGEM"

    # ------------------ GET BY ID -------------------

    def test_get_commission_types_by_id(self, client):
        response = client.get("/commission_types/10")
        assert response.status_code == 200
        assert len(response.json) == 2
        assert response.json["id"] == 10
        assert response.json["name"] == "INVESTIGAÇÃO EPIDEMIOLÓGICA"
