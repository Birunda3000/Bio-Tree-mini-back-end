from app.main.model import InstitutionType


def create_base_seed_institution_type(db):
    """Add 3 institution type"""

    institution_type = InstitutionType(name="INSTITUTION TYPE ONE")
    db.session.add(institution_type)

    institution_type = InstitutionType(name="INSTITUTION TYPE TWO")
    db.session.add(institution_type)

    institution_type = InstitutionType(name="INSTITUTION TYPE THREE")
    db.session.add(institution_type)

    db.session.commit()
