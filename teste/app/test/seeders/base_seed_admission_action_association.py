from app.main.model import AdmissionActionAssociation


def create_base_seed_admission_action_association(db):
    """Add 2 admission action association"""

    new_sae = AdmissionActionAssociation(admission_id=1, action_id=1, recurrence="1/1")

    db.session.add(new_sae)

    new_sae = AdmissionActionAssociation(admission_id=1, action_id=2, recurrence="2/2")

    db.session.add(new_sae)

    db.session.commit()
