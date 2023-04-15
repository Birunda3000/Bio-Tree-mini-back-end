from app.main.model import InstitutionSubtype


def create_base_seed_institution_subtype(db):
    """Add 3 institution subtype"""

    institution_subtype = InstitutionSubtype(
        institution_type_id=1, name="INSTITUTION SUBTYPE ONE"
    )
    db.session.add(institution_subtype)

    institution_subtype = InstitutionSubtype(
        institution_type_id=1, name="INSTITUTION SUBTYPE TWO"
    )
    db.session.add(institution_subtype)

    institution_subtype = InstitutionSubtype(
        institution_type_id=3, name="INSTITUTION SUBTYPE THREE"
    )
    db.session.add(institution_subtype)

    db.session.commit()
