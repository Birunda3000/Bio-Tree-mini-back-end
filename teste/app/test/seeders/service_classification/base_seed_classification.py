from app.main.model import Classification


def create_base_seed_classification(db):
    """Add 2 classification"""

    classification = Classification(service_id=1, code="001", name="CLASSIFICATION ONE")
    db.session.add(classification)

    classification = Classification(service_id=1, code="002", name="CLASSIFICATION TWO")
    db.session.add(classification)

    db.session.commit()
