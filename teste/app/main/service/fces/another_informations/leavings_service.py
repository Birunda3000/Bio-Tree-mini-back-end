from app.main import db
from app.main.exceptions import DefaultException
from app.main.model import Leavings

LEAVINGS = [
    "RESÍDUOS BIOLÓGICOS",
    "RESÍDUOS QUÍMICOS",
    "REJEITOS RADIOATIVOS",
    "RESÍDUOS COMUNS",
    "NENHUM",
]


def get_leavings(options: list = None):
    query = Leavings.query

    if options is not None:
        query = query.options(*options)

    leavings = query.all()
    return leavings


def create_default_leavings():
    for _leavings in LEAVINGS:
        leavings = Leavings(name=_leavings)
        db.session.add(leavings)
    db.session.commit()


def get_leavings_by_id(leavings_id: int, options: list = None) -> Leavings:

    query = Leavings.query

    if options is not None:
        query = query.options(*options)

    leavings = query.get(leavings_id)

    if leavings is None:
        raise DefaultException("leavings_not_found", code=404)

    return leavings


def validate_leavings(leavings_ids: set[int]) -> list[Leavings]:

    leavings = Leavings.query.filter(Leavings.id.in_(leavings_ids)).all()

    leavings_ids_db = set(leaving.id for leaving in leavings)

    if leavings_ids != leavings_ids_db:
        raise DefaultException("leavings_not_found", code=404)
    return leavings
