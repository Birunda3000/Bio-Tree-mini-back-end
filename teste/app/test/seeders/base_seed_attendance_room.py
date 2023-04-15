from app.main.model.attendance_room_model import AttendanceRoom


def create_base_seed_attendance_room(db):
    """Add 2 attendance_rooms"""

    new_attendance_room = AttendanceRoom(
        acronym="AAA", description="sala A", call_panel_id=1
    )
    db.session.add(new_attendance_room)

    new_attendance_room = AttendanceRoom(
        acronym="BBB", description="sala B", call_panel_id=2
    )
    db.session.add(new_attendance_room)

    db.session.commit()
