from app.main.model import Leavings


def create_base_seed_leavings(db):

    new_leavings = Leavings(name="RESÍDUOS BIOLÓGICOS")

    db.session.add(new_leavings)

    new_leavings = Leavings(name="RESÍDUOS QUÍMICOS")

    db.session.add(new_leavings)

    new_leavings = Leavings(name="REJEITOS RADIOATIVOS")

    db.session.add(new_leavings)

    new_leavings = Leavings(name="RESÍDUOS COMUNS")

    db.session.add(new_leavings)

    new_leavings = Leavings(name="NENHUM")

    db.session.add(new_leavings)

    db.session.commit()
