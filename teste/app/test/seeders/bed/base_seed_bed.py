from app.main.model.bed.bed_model import Bed


def create_base_seed_bed(db):
    """Add 2 beds"""

    new_bed = Bed(bed_number=1, available=True, status=False, room_id=1)
    db.session.add(new_bed)

    new_bed = Bed(bed_number=2, available=True, status=False, room_id=1)
    db.session.add(new_bed)

    new_bed = Bed(bed_number=3, available=True, status=False, room_id=1)
    db.session.add(new_bed)

    new_bed = Bed(bed_number=1, available=False, status=True, room_id=2)
    db.session.add(new_bed)

    new_bed = Bed(bed_number=2, available=True, status=False, room_id=2)
    db.session.add(new_bed)

    new_bed = Bed(bed_number=3, available=True, status=False, room_id=2)
    db.session.add(new_bed)

    db.session.commit()
