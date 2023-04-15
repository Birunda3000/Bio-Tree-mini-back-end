from app.main.model import UnitMeasurement


def create_base_seed_unit_measurement(db):
    new_unit_measurement = UnitMeasurement(name="UNIT MEASUREMENT ONE")

    db.session.add(new_unit_measurement)

    new_unit_measurement = UnitMeasurement(name="UNIT MEASUREMENT TWO")

    db.session.add(new_unit_measurement)

    new_unit_measurement = UnitMeasurement(name="UNIT MEASUREMENT THREE")

    db.session.add(new_unit_measurement)

    db.session.commit()
