from app.main.model.bed.bed_type_model import BedType


def create_base_seed_bed_type(db):
    bed_type = BedType(
        name="tipo de leito teste 1",
    )
    db.session.add(bed_type)

    bed_type = BedType(
        name="tipo de leito teste 2",
    )
    db.session.add(bed_type)

    db.session.commit()
