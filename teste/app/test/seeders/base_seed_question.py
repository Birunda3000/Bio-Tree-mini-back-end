from app.main.model import Question


def create_base_seed_question(db):

    new_question = Question(name="PERGUNTA1")
    db.session.add(new_question)

    new_question = Question(name="PERGUNTA2")
    db.session.add(new_question)

    db.session.commit()
