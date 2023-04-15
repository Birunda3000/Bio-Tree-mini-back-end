from app.main.model import Vaccine, VaccineLaboratory


def create_base_seed_vaccine(db):
    """Add 2 vaccines"""

    laboratories = VaccineLaboratory.query.order_by(VaccineLaboratory.id).all()

    new_vaccine = Vaccine(
        name="VACINA TESTE 1",
        pni_code="00123",
        belongs_to_vaccine_card=True,
        current=True,
        export_to_esus=False,
        controls_vaccine_batch=True,
        oblige_establishment=False,
        laboratories=laboratories,
    )

    db.session.add(new_vaccine)

    new_vaccine = Vaccine(
        name="VACINA TESTE 2",
        pni_code="00123",
        belongs_to_vaccine_card=True,
        current=True,
        export_to_esus=True,
        controls_vaccine_batch=True,
        oblige_establishment=True,
        laboratories=[laboratories[0]],
    )
    db.session.add(new_vaccine)

    db.session.commit()
