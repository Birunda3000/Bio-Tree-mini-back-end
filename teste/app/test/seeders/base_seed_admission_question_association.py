from app.main.model import AdmissionQuestionAssociation


def create_base_seed_admission_question_association(db):
    """Add 2 admission question association"""

    new_sae = AdmissionQuestionAssociation(admission_id=1, question_id=1)

    db.session.add(new_sae)

    new_sae = AdmissionQuestionAssociation(admission_id=1, question_id=2)

    db.session.add(new_sae)
    db.session.commit()
