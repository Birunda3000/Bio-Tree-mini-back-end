import pytest

@pytest.fixture()
def base_attendance_room():
    """Base attendance room data"""
    attendance_room = {
        "acronym": "CCC", 
        "description": "sala C", 
        "call_panel_id": 1
    }
    return attendance_room

@pytest.fixture()
def base_attendance_room_update():
    """Base attendance room data"""
    attendance_room = {
        "acronym": "AAA edit", 
        "description": "sala A edit", 
        "call_panel_id": 1
    }
    return attendance_room

@pytest.fixture()
def base_attendance_room_update_acronym_in_use():
    """Base attendance room data"""
    attendance_room = {
        "acronym": "BBB", 
        "description": "sala F", 
        "call_panel_id": 1
    }
    return attendance_room

@pytest.fixture()
def base_attendance_room_update_description_in_use():
    """Base attendance room data"""
    attendance_room = {
        "acronym": "JJJ", 
        "description": "sala B", 
        "call_panel_id": 1
    }
    return attendance_room

@pytest.fixture()
def base_attendance_room_not_found():
    """Base attendance room data"""
    attendance_room = {
        "acronym": "DDD", 
        "description": "sala D", 
        "call_panel_id": 1
    }
    return attendance_room

@pytest.fixture()
def base_attendance_room_call_panel_not_found():
    """Base attendance room data"""
    attendance_room = {
        "acronym": "EEE", 
        "description": "sala E", 
        "call_panel_id": 0
    }
    return attendance_room