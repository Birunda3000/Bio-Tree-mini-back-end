from app.main.model import Procedure


def create_base_seed_procedure(db):
    """Add 3 procedures"""

    new_procedure = Procedure(
        code="9965",
        classification="06.04.36.004",
        dv=5,
        description="ATORVASTATINA 80 MG (POR COMPRIMIDO)",
        price="0.00",
    )

    db.session.add(new_procedure)

    new_procedure = Procedure(
        code="9911",
        classification="06.04.27.001",
        dv=1,
        description="BEZAFIBRATO 200 MG (POR DRAGEA OU COMPRIMIDO)",
        price="0.00",
    )

    db.session.add(new_procedure)

    new_procedure = Procedure(
        code="10371",
        classification="06.03.05.011",
        dv=5,
        description="TENECTEPLASE 40 MG INJETAVEL (POR FRASCO AMPOLA) DE USO NAS URGENCIAS PRE-HOSPITALARES",
        price="1810.00",
    )

    db.session.add(new_procedure)

    db.session.commit()
