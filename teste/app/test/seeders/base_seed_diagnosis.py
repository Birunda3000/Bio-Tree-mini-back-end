from app.main.model import Diagnosis, Question


def create_base_seed_diagnosis(db):
    question = Question.query.get(1)

    new_diagnosis = Diagnosis(questions=[question], protocol_id=1)

    db.session.add(new_diagnosis)

    new_diagnosis = Diagnosis(questions=[question], protocol_id=6)

    db.session.add(new_diagnosis)
    db.session.commit()
