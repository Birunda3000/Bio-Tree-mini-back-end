import pytest
from sqlalchemy.orm import joinedload

from app.main import db
from app.main.model import Bed, Room
from app.test.seeders import create_base_seed_bed, create_base_seed_room


@pytest.fixture(scope="module")
def seeded_database(client, database):
    """Seed database with rooms and beds"""
    create_base_seed_room(db)
    create_base_seed_bed(db)


@pytest.mark.usefixtures("seeded_database")
class TestRoomController:

    # --------------------- GET ROOMS ---------------------
    def test_get_rooms(self, client):
        response = client.get("/room")

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 3
        assert response.json["total_pages"] == 1
        assert response.json["items"][0]["name"] == "SALA TESTE 1"
        assert response.json["items"][0]["total_beds"] == 3
        assert response.json["items"][0]["total_available_beds"] == 0
        assert response.json["items"][1]["name"] == "SALA TESTE 2"
        assert response.json["items"][1]["total_beds"] == 3
        assert response.json["items"][1]["total_available_beds"] == 0

    @pytest.mark.parametrize(
        "name",
        ["SALA TESTE 1", "1"],
        ids=["complete_name", "incomplete_name"],
    )
    def test_get_rooms_by_name(self, client, name):
        response = client.get("/room", query_string={"name": name})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["total_items"] == 1
        assert response.json["items"][0]["name"] == "SALA TESTE 1"

    @pytest.mark.parametrize(
        "available,status",
        [(True, False), (False, True), (False, False)],
        ids=[
            "only_available_false",
            "only_status_false",
            "both_available_and_status_false",
        ],
    )
    def test_get_room_with_unavailable_bed(self, client, available, status):

        new_bed = Bed(available=available, status=status, room_id=3)

        db.session.add(new_bed)
        db.session.flush()

        response = client.get("/room", query_string={"name": "SALA TESTE 3"})

        db.session.rollback()

        assert response.status_code == 200
        assert response.json["items"][0]["total_beds"] == 1
        assert response.json["items"][0]["total_available_beds"] == 0

    def test_get_room_with_available_bed(self, client):
        bed = Bed.query.get(1)
        bed.status = True
        db.session.add(bed)
        db.session.commit()

        response = client.get("/room", query_string={"name": "SALA TESTE 1"})

        assert response.status_code == 200
        assert response.json["items"][0]["total_beds"] == 3
        assert response.json["items"][0]["total_available_beds"] == 1

    # --------------------- UPDATE ROOM ---------------------

    def test_update_room_with_registered_name(self, client):
        response = client.put("/room/1", json={"name": "SALA TESTE 2"})

        assert response.status_code == 409
        assert response.json["message"] == "name_in_use"

    def test_update_non_registered_room(self, client):
        response = client.put("/room/0", json={"name": "SALA TESTE 3"})

        assert response.status_code == 404
        assert response.json["message"] == "room_not_found"

    def test_update_room_with_empty_name(self, client):
        response = client.put("/room/1", json={"name": ""})

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert "name" in response.json["errors"].keys()

    def test_update_room(self, client):
        response = client.put("/room/1", json={"name": "SALA MODIFICADA"})

        assert response.status_code == 200
        assert response.json["message"] == "room_updated"

        room = Room.query.get(1)
        assert room.name == "SALA MODIFICADA"

    # --------------------- CREATE ROOM ---------------------

    def test_create_room_with_registered_name(self, client):
        response = client.post(
            "/room", json={"name": "SALA TESTE 2", "number_of_beds": 2}
        )

        assert response.status_code == 409
        assert response.json["message"] == "name_in_use"

    def test_create_room_with_zero_beds(self, client):
        response = client.post(
            "/room", json={"name": "SALA TESTE 4", "number_of_beds": 0}
        )

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert "number_of_beds" in response.json["errors"].keys()

    def test_create_room_with_empty_name(self, client):
        response = client.post("/room", json={"name": ""})

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert "name" in response.json["errors"].keys()

    def test_create_room(self, client):
        response = client.post(
            "/room", json={"name": "SALA TESTE 4", "number_of_beds": 2}
        )

        assert response.status_code == 201
        assert response.json["message"] == "room_created"

        room = (
            Room.query.options(joinedload("beds"))
            .filter_by(name="SALA TESTE 4")
            .first()
        )

        assert room.name == "SALA TESTE 4"
        assert len(room.beds) == 2
        assert room.beds[0].bed_number == 1
        assert room.beds[1].bed_number == 2
