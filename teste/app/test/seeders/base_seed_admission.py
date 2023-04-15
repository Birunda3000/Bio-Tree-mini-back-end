from app.main.model import Admission


def create_base_seed_admission(db):

    new_admission = Admission(
        patient_id=1,
        professional_id=1,
        bed_id=1,
        type="Observação",
    )
    db.session.add(new_admission)

    new_admission = Admission(
        patient_id=2,
        professional_id=2,
        bed_id=5,
        type="Internação",
    )
    db.session.add(new_admission)

    db.session.commit()
