from app.main import db
from app.main.exceptions import DefaultException
from app.main.model import Cid10


def create_default_cid_10():
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


def get_cid_10_by_code(cid_10_code: str) -> list[tuple[str, any]]:
    return Cid10.query.filter(Cid10.code.ilike(f"%{cid_10_code}%")).all()


def get_cid_10(cid_10_id: int, options: list = None) -> Cid10:

    query = Cid10.query

    if options is not None:
        query = query.options(*options)

    cid_10 = query.get(cid_10_id)

    if cid_10 is None:
        raise DefaultException("cid_10_not_found", code=404)

    return cid_10
