from app.main.model import VaccineLaboratory


def create_base_seed_vaccine_laboratory(db):
    """Add 2 vaccine laboratories"""

    new_vaccine_laboratory = VaccineLaboratory(
        name="LABORATORIO TESTE 1", pni_code="COD001", cnpj="88649316000150"
    )
    db.session.add(new_vaccine_laboratory)

    new_vaccine_laboratory = VaccineLaboratory(
        name="LABORATORIO TESTE 2", pni_code="COD002", cnpj="35490474000143"
    )
    db.session.add(new_vaccine_laboratory)

    db.session.commit()
