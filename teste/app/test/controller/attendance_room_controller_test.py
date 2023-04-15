import pytest

from app.main import db
from app.test.seeders import (
    create_base_seed_attendance_room,
    create_base_seed_call_panel,
)


@pytest.fixture(scope="module")
def seeded_database(database):
    create_base_seed_call_panel(db)
    create_base_seed_attendance_room(db)


@pytest.mark.usefixtures("seeded_database")
class TestAttendanceRoomController:
    # --------------------- GET ATTENDANCE ROOM ---------------------

    def test_get_all_attendance_rooms(self, client):
        response = client.get("/attendance_room")
        assert response.status_code == 200
        assert len(response.json) == 4
        assert len(response.json["items"]) == 2
        assert response.json["items"][0]["acronym"] == "AAA"

    def test_get_attendance_room_by_id_id(self, client):
        response = client.get("/attendance_room/1")
        assert response.status_code == 200
        assert response.json["acronym"] == "AAA"

    def test_get_attendance_room_by_id_acronym(self, client):
        response = client.get("/attendance_room?acronym=AAA")
        assert response.status_code == 200

        assert len(response.json["items"]) == 1
        assert response.json["items"][0]["acronym"] == "AAA"

    def test_get_attendance_room_by_id_description(self, client):
        response = client.get(
            "/attendance_room", query_string={"description": "sala A"}
        )
        assert response.status_code == 200
        assert len(response.json["items"]) == 1
        assert response.json["items"][0]["description"] == "sala A"

    def test_get_attendance_room_by_id_id_not_found(self, client):
        response = client.get("/attendance_room/0")
        assert response.status_code == 404

    # --------------------- POST ATTENDANCE ROOM ---------------------

    def test_create_attendance_room(self, client, base_attendance_room):
        response = client.post(
            "/attendance_room",
            json=base_attendance_room,
        )
        assert response.status_code == 201
        assert response.json["message"] == "attendance_room_created"
    
    def test_create_attendance_room_acronym_in_use(self, client, base_attendance_room_update_acronym_in_use):
        response = client.post(
            "/attendance_room",
            json=base_attendance_room_update_acronym_in_use,
        )
        assert response.status_code == 409
        assert response.json["message"] == "acronym_in_use"

    def test_create_attendance_room_description_in_use(self, client, base_attendance_room_update_description_in_use):
        response = client.post(
            "/attendance_room",
            json=base_attendance_room_update_description_in_use,
        )
        assert response.status_code == 409
        assert response.json["message"] == "description_in_use"

    def test_create_attendance_room_without_acronym(self, client):
        response = client.post(
            "/attendance_room", json={"description": "sala A", "call_panel_id": 1}
        )
        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"

    def test_create_attendance_room_without_description(self, client):
        response = client.post(
            "/attendance_room", json={"acronym": "CCC", "call_panel_id": 1}
        )
        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
    
    def test_create_attendance_room_without_call_panel_id(self, client):
        response = client.post(
            "/attendance_room", json={"acronym": "CCC", "description": "sala C"}
        )
        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
    
    def test_create_attendance_room_with_invalid_call_panel_id(self, client, base_attendance_room_call_panel_not_found):
        response = client.post(
            "/attendance_room",
            json=base_attendance_room_call_panel_not_found,
        )
        assert response.status_code == 404
        assert response.json["message"] == "call_panel_not_found"


    # --------------------- PUT ATTENDANCE ROOM ---------------------

    def test_update_attendance_room(self, client, base_attendance_room_update):
        response = client.put(
            "/attendance_room/1",
            json=base_attendance_room_update,
        )
        assert response.status_code == 200
        assert response.json["message"] == "attendance_room_updated"

    def test_update_attendance_room_acronym_in_use(self, client, base_attendance_room_update_acronym_in_use):
        response = client.put(
            "/attendance_room/1",
            json=base_attendance_room_update_acronym_in_use,
        )
        assert response.status_code == 409
        assert response.json["message"] == "acronym_in_use"

    def test_update_attendance_room_description_in_use(self, client,base_attendance_room_update_description_in_use):
        response = client.put(
            "/attendance_room/1",
            json=base_attendance_room_update_description_in_use,
        )
        assert response.status_code == 409
        assert response.json["message"] == "description_in_use"

    def test_update_attendance_room_not_found(self, client, base_attendance_room_not_found):
        response = client.put(
            "/attendance_room/0",
            json=base_attendance_room_not_found,
        )
        assert response.status_code == 404
        assert response.json["message"] == "attendance_room_not_found"

    def test_update_attendance_room_without_acronym(self, client):
        response = client.put(
            "/attendance_room/1", json={"description": "sala A", "call_panel_id": 1}
        )
        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"

    def test_update_attendance_room_without_description(self, client):
        response = client.put(
            "/attendance_room/1", json={"acronym": "CCC", "call_panel_id": 1}
        )
        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
    
    def test_update_attendance_room_call_panel_not_found(self, client, base_attendance_room_call_panel_not_found):
        response = client.put(
            "/attendance_room/1",
            json=base_attendance_room_call_panel_not_found,
        )
        assert response.status_code == 404
        assert response.json["message"] == "call_panel_not_found"

    # --------------------- DELETE ATTENDANCE ROOM ---------------------

    def test_delete_attendance_room_not_found(self, client):
        response = client.delete("/attendance_room/0")
        assert response.status_code == 404
        assert response.json["message"] == "attendance_room_not_found"

    def test_delete_attendance_room(self, client):
        response = client.delete("/attendance_room/1")
        assert response.status_code == 200
        assert response.json["message"] == "attendance_room_deleted"
