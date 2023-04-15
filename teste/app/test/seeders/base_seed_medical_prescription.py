from app.main.model import (
    MedicalPrescription,
    MedicalPrescriptionMedicine,
    MedicalPrescriptionOrientation,
    MedicalPrescriptionProcedure,
)
from app.main.service import datetime_from_string


def create_base_seed_medical_prescription(db):
    new_medical_prescription = MedicalPrescription(
        professional_id=1, patient_id=1, room_id=1
    )

    db.session.add(new_medical_prescription)

    new_orientation = MedicalPrescriptionOrientation(
        medical_prescription=new_medical_prescription,
        orientation="Orientation One",
        execute_at=datetime_from_string("25/08/1989 20:00:00"),
        observations="Orientation Observation One",
    )

    db.session.add(new_orientation)

    new_medicine = MedicalPrescriptionMedicine(
        medical_prescription=new_medical_prescription,
        medicine_id=1,
        execute_at=datetime_from_string("25/08/1989 20:00:00"),
        observations="Medicine Observation One",
    )

    db.session.add(new_medicine)

    new_procedure = MedicalPrescriptionProcedure(
        medical_prescription=new_medical_prescription,
        procedure_id=1,
        execute_at=datetime_from_string("25/08/1989 20:00:00"),
        observations="Procedure Observation One",
    )

    db.session.add(new_procedure)

    new_medical_prescription = MedicalPrescription(
        professional_id=2, patient_id=2, room_id=2
    )

    db.session.add(new_medical_prescription)

    new_orientation = MedicalPrescriptionOrientation(
        medical_prescription=new_medical_prescription,
        orientation="Orientation Two",
        execute_at=datetime_from_string("29/09/1989 19:00:00"),
        observations="Orientation Observation Two",
    )

    db.session.add(new_orientation)

    new_medicine = MedicalPrescriptionMedicine(
        medical_prescription=new_medical_prescription,
        medicine_id=2,
        execute_at=datetime_from_string("29/09/1989 19:00:00"),
        observations="Medicine Observation Two",
    )

    db.session.add(new_medicine)

    new_procedure = MedicalPrescriptionProcedure(
        medical_prescription=new_medical_prescription,
        procedure_id=2,
        execute_at=datetime_from_string("29/09/1989 19:00:00"),
        observations="Procedure Observation Two",
    )

    db.session.add(new_procedure)

    db.session.commit()
