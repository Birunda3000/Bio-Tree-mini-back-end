from app.main.model import Cooperative


def create_base_seed_cooperative(db):
    cooperative = Cooperative(
        name="Cooperativa teste 1",
        cbo="CBO1",
    )
    db.session.add(cooperative)

    cooperative = Cooperative(
        name="Cooperativa teste 2",
        cbo="CBO2",
    )
    db.session.add(cooperative)

    db.session.commit()
