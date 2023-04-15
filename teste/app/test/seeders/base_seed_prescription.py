from app.main.model.action_model import Action
from app.main.model.prescription_model import Prescription


def create_base_seed_prescription(db):

    action = Action.query.get(1)

    new_prescription = Prescription(actions=[action], protocol_id=2)
    db.session.add(new_prescription)

    new_prescription = Prescription(actions=[action], protocol_id=4)
    db.session.add(new_prescription)

    db.session.commit()
