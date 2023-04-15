from app.main.model.sanitary_district_model import SanitaryDistrict


def create_base_seed_sanitary_district(db):
    """Add 2 sanitary districts"""

    new_sanitary_district = SanitaryDistrict(name="DISTRITO SANITÁRIO TESTE 1")
    db.session.add(new_sanitary_district)

    new_sanitary_district = SanitaryDistrict(name="DISTRITO SANITÁRIO TESTE 2")
    db.session.add(new_sanitary_district)

    db.session.commit()
