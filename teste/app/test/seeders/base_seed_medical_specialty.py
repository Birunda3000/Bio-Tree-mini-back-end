from app.main.model import MedicalSpecialty


def create_base_seed_medical_specialty(db):
    new_medical_specialty = MedicalSpecialty(name="MEDICAL SPECIALTY ONE")

    db.session.add(new_medical_specialty)

    new_medical_specialty = MedicalSpecialty(name="MEDICAL SPECIALTY TWO")

    db.session.add(new_medical_specialty)

    new_medical_specialty = MedicalSpecialty(name="MEDICAL SPECIALTY THREE")

    db.session.add(new_medical_specialty)

    db.session.commit()
