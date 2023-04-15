from app.main.model import DeathLaunch, Patient
from app.main.service import datetime_from_string


def create_base_death_launch(db):
    patients = Patient.query.filter(Patient.id.in_([1, 2])).order_by(Patient.id).all()

    death_launch = DeathLaunch(
        patient=patients[0],
        cid_10_id=1,
        professional_id=1,
        certificate_number=1,
        circunstances_of_death="circustancia teste 1",
        place="Sala X",
        datetime_of_death=datetime_from_string("25/08/1989 18:00:00"),
        registration_datetime=datetime_from_string("25/08/1989 23:40:00"),
    )
    db.session.add(death_launch)

    death_launch = DeathLaunch(
        patient=patients[1],
        cid_10_id=2,
        professional_id=2,
        certificate_number=2,
        place="Sala Y",
        circunstances_of_death="circustancia teste 2",
        datetime_of_death=datetime_from_string("25/08/2005 18:00:00"),
        registration_datetime=datetime_from_string("25/08/2005 23:40:00"),
    )
    db.session.add(death_launch)
    db.session.commit()
