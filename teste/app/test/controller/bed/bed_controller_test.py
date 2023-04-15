import pytest

from app.main import db
from app.main.model import Bed
from app.test.seeders import create_base_seed_bed, create_base_seed_room


@pytest.fixture(scope="module")
def seeded_database(client, database):
    """Seed database with rooms and beds"""
    create_base_seed_room(db)
    return create_base_seed_bed(db)


@pytest.mark.usefixtures("seeded_database")
class TestBedController:

    # --------------------- GET BED ---------------------
    def test_get_bed(self, client):
        response = client.get("/bed")

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 6
        assert response.json["total_pages"] == 1
        assert response.json["items"][0]["bed_number"] == 1
        assert response.json["items"][0]["available"] == True
        assert response.json["items"][0]["status"] == False
        assert response.json["items"][0]["room_id"] == 1
        assert response.json["items"][1]["bed_number"] == 2
        assert response.json["items"][1]["available"] == True
        assert response.json["items"][1]["status"] == False
        assert response.json["items"][1]["room_id"] == 1
        assert response.json["items"][2]["bed_number"] == 3
        assert response.json["items"][2]["available"] == True
        assert response.json["items"][2]["status"] == False
        assert response.json["items"][2]["room_id"] == 1
        assert response.json["items"][3]["bed_number"] == 1
        assert response.json["items"][3]["available"] == False
        assert response.json["items"][3]["status"] == True
        assert response.json["items"][3]["room_id"] == 2
        assert response.json["items"][4]["bed_number"] == 2
        assert response.json["items"][4]["available"] == True
        assert response.json["items"][4]["status"] == False
        assert response.json["items"][4]["room_id"] == 2
        assert response.json["items"][5]["bed_number"] == 3
        assert response.json["items"][5]["available"] == True
        assert response.json["items"][5]["status"] == False
        assert response.json["items"][5]["room_id"] == 2

    def test_get_bed_by_page(self, client):
        response = client.get("/bed", query_string={"page": 2})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert len(response.json["items"]) == 0
        assert response.json["current_page"] == 2

    def test_get_bed_by_bed_number(self, client):
        response = client.get("/bed", query_string={"bed_number": 1})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 2
        assert response.json["total_pages"] == 1
        assert response.json["items"][0]["bed_number"] == 1
        assert response.json["items"][0]["room_id"] == 1
        assert response.json["items"][1]["bed_number"] == 1
        assert response.json["items"][1]["room_id"] == 2

    def test_get_bed_with_invalid_bed_number(self, client):
        response = client.get("/bed", query_string={"bed_number": 123})
        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["items"] == []

    def test_get_bed_by_available(self, client):
        response = client.get("/bed", query_string={"available": True})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 5
        assert response.json["total_pages"] == 1
        assert response.json["items"][0]["bed_number"] == 1
        assert response.json["items"][0]["available"] == True
        assert response.json["items"][0]["room_id"] == 1
        assert response.json["items"][1]["bed_number"] == 2
        assert response.json["items"][1]["available"] == True
        assert response.json["items"][1]["room_id"] == 1
        assert response.json["items"][2]["bed_number"] == 3
        assert response.json["items"][2]["available"] == True
        assert response.json["items"][2]["room_id"] == 1
        assert response.json["items"][3]["bed_number"] == 2
        assert response.json["items"][3]["available"] == True
        assert response.json["items"][3]["room_id"] == 2
        assert response.json["items"][4]["bed_number"] == 3
        assert response.json["items"][4]["available"] == True
        assert response.json["items"][4]["room_id"] == 2

    def test_get_hospita_bed_with_available_false(self, client):
        response = client.get("/bed", query_string={"available": False})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 1
        assert response.json["total_pages"] == 1
        assert response.json["items"][0]["bed_number"] == 1
        assert response.json["items"][0]["available"] == False
        assert response.json["items"][0]["status"] == True
        assert response.json["items"][0]["room_id"] == 2

    def test_get_bed_by_status(self, client):
        response = client.get("/bed", query_string={"status": True})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 1
        assert response.json["total_pages"] == 1
        assert response.json["items"][0]["bed_number"] == 1
        assert response.json["items"][0]["status"] == True
        assert response.json["items"][0]["room_id"] == 2

    def test_get_bed_by_with_status_false(self, client):
        response = client.get("/bed", query_string={"status": False})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 5
        assert response.json["total_pages"] == 1
        assert response.json["items"][0]["bed_number"] == 1
        assert response.json["items"][0]["available"] == True
        assert response.json["items"][0]["status"] == False
        assert response.json["items"][0]["room_id"] == 1
        assert response.json["items"][1]["bed_number"] == 2
        assert response.json["items"][1]["available"] == True
        assert response.json["items"][1]["status"] == False
        assert response.json["items"][1]["room_id"] == 1
        assert response.json["items"][2]["bed_number"] == 3
        assert response.json["items"][2]["available"] == True
        assert response.json["items"][2]["status"] == False
        assert response.json["items"][2]["room_id"] == 1
        assert response.json["items"][3]["bed_number"] == 2
        assert response.json["items"][3]["available"] == True
        assert response.json["items"][3]["status"] == False
        assert response.json["items"][3]["room_id"] == 2
        assert response.json["items"][4]["bed_number"] == 3
        assert response.json["items"][4]["available"] == True
        assert response.json["items"][4]["status"] == False
        assert response.json["items"][4]["room_id"] == 2

    def test_get_bed_by_room_id(self, client):
        response = client.get("/bed", query_string={"room_id": 2})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 3
        assert response.json["total_pages"] == 1
        assert response.json["items"][0]["bed_number"] == 1
        assert response.json["items"][0]["available"] == False
        assert response.json["items"][0]["room_id"] == 2
        assert response.json["items"][1]["bed_number"] == 2
        assert response.json["items"][1]["available"] == True
        assert response.json["items"][1]["room_id"] == 2
        assert response.json["items"][2]["bed_number"] == 3
        assert response.json["items"][2]["available"] == True
        assert response.json["items"][2]["room_id"] == 2

    def test_get_bed_with_invalid_room_id(self, client):
        response = client.get("/bed", query_string={"room_id": 100})
        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["items"] == []

    # --------------------- UPDATE BED ---------------------

    def test_update_non_registered_bed(self, client):
        response = client.patch("/bed/0", json={"status": False})

        assert response.status_code == 404
        assert response.json["message"] == "bed_not_found"

    def test_update_bed_status(self, client):
        response = client.patch("/bed/1", json={"status": True})

        assert response.status_code == 200
        assert response.json["message"] == "bed_updated"

    # --------------------- CREATE BED ---------------------
    def test_create_bed_with_unregistered_room(self, client):
        response = client.post("/bed", json={"status": True, "room_id": 0})

        assert response.status_code == 404
        assert response.json["message"] == "room_not_found"

    def test_create_bed_with_invalid_room_format(self, client):
        response = client.post(
            "/bed", json={"available": True, "status": True, "room_id": "1"}
        )
        assert response.status_code == 400

    def test_create_bed_with_no_room_id(self, client):
        response = client.post("/bed", json={"available": False, "status": False})
        assert response.status_code == 400

    def test_create_bed_with_invalid_available_format(self, client):
        response = client.post(
            "/bed", json={"available": False, "status": "True", "room_id": 1}
        )
        assert response.status_code == 400

    def test_create_bed_with_invalid_status_format(self, client):
        response = client.post(
            "/bed", json={"available": True, "status": "False", "room_id": 1}
        )
        assert response.status_code == 400

    @pytest.mark.parametrize(
        "room_id,expected_bed_number, bed_id",
        [(1, 4, 7), (3, 1, 8)],
        ids=["room_already_with_beds", "room_with_no_beds"],
    )
    def test_create_bed(self, client, room_id, expected_bed_number, bed_id):
        response = client.post("/bed", json={"status": True, "room_id": room_id})

        assert response.status_code == 201
        assert response.json["message"] == "bed_created"

        bed = Bed.query.get(bed_id)

        assert bed.bed_number == expected_bed_number
        assert bed.status == True
        assert bed.available == True
        assert bed.room_id == room_id
