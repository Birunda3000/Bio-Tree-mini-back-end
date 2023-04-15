from app.main.model import Cid10


def create_base_seed_cid_10(db):
    cid_10 = Cid10(
        code="S02",
        category=19,
    )
    db.session.add(cid_10)
    cid_10 = Cid10(
        code="S022",
        category=19,
    )
    db.session.add(cid_10)
    db.session.commit()
