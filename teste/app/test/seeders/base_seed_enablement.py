from app.main.model import Enablement
from app.main.service import date_from_string


def create_base_seed_enablement(db):
    new_enablement = Enablement(
        code="0001",
        name="HABILITAÇÃO TESTE 1",
        number_of_beds=100,
        ordinance_number=1,
        release_date=date_from_string("01/01/1990"),
    )
    db.session.add(new_enablement)

    new_enablement = Enablement(
        code="0002",
        name="HABILITAÇÃO TESTE 2",
        number_of_beds=100,
        ordinance_number=2,
        release_date=date_from_string("01/01/1990"),
    )
    db.session.add(new_enablement)

    db.session.commit()
