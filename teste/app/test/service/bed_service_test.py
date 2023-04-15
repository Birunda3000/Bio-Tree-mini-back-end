import pytest

from app.main import db
from app.main.exceptions import DefaultException
from app.main.model import Bed, Room
from app.main.service import (
    create_hospital_first_beds,
    update_bed,
    update_bed_available_field,
)
from app.test.seeders import create_base_seed_bed, create_base_seed_room


@pytest.fixture(scope="module")
def seeded_database(client, database):
    """Seed database with rooms and beds"""
    create_base_seed_room(db)
    create_base_seed_bed(db)


@pytest.mark.usefixtures("seeded_database")
class TestBedController:

    # --------------------- UPDATE BED AVAILABLE FIELD ---------------------

    @pytest.mark.parametrize(
        "bed_id,available",
        [(4, True), (1, False)],
        ids=["available_equals_true", "available_equals_false"],
    )
    def test_update_bed_available_field(self, bed_id, available):
        update_bed_available_field(bed_id=bed_id, available=available)
        db.session.flush()

        bed = Bed.query.get(bed_id)

        assert bed.available == available

        db.session.rollback()

    def test_update_unregistered_bed_available_field(self):
        with pytest.raises(DefaultException, match="bed_not_found"):
            update_bed_available_field(bed_id=0, available=True)

    @pytest.mark.parametrize(
        "bed_id,available,expected_raise_message",
        [(1, True, "bed_already_available"), (4, False, "bed_already_unavailable")],
        ids=["available_equals_true", "available_equals_false"],
    )
    def test_update_bed_available_field_with_equals_information(
        self, bed_id, available, expected_raise_message
    ):
        with pytest.raises(DefaultException, match=expected_raise_message):
            update_bed_available_field(bed_id=bed_id, available=available)

    # --------------------- CREATE BEDS ---------------------

    def test_create_hospital_first_beds(self):
        room = Room.query.get(3)

        create_hospital_first_beds(number_of_beds=2, room=room)
        db.session.commit()

        beds = Bed.query.filter(Bed.room == room).all()

        assert len(beds) == 2
        assert beds[0].bed_number == 1
        assert beds[1].bed_number == 2
