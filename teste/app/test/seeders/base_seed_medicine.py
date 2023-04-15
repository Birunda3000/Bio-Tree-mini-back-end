from app.main.model import Medicine


def create_base_seed_medicine(db):
    new_medicine = Medicine(name="Medicine One")

    db.session.add(new_medicine)

    new_medicine = Medicine(name="Medicine Two")

    db.session.add(new_medicine)

    new_medicine = Medicine(name="Medicine Three")

    db.session.add(new_medicine)

    new_medicine = Medicine(name="Medicine Four")

    db.session.add(new_medicine)

    new_medicine = Medicine(name="Medicine Five")

    db.session.add(new_medicine)

    db.session.commit()
