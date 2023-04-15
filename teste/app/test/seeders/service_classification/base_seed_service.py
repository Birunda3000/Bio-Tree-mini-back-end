from app.main.model import Service


def create_base_seed_service(db):
    """Add 2 service"""

    service = Service(code="001", name="SERVICE ONE")
    db.session.add(service)

    service = Service(code="002", name="SERVICE TWO")
    db.session.add(service)

    db.session.commit()
