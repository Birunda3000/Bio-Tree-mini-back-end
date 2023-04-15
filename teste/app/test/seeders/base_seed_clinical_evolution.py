from app.main.model import (
    History,
    HistoryMedicalPrescriptionMedicine,
    HistoryMedicalPrescriptionOrientation,
    HistoryMedicalPrescriptionProcedure,
)
from app.main.service import datetime_from_string


def create_base_seed_clinical_evolution(db):

    new_history = History(admission_id=1, professional_id=1, type="Clínico")

    new_history_medical_prescription_medicine = HistoryMedicalPrescriptionMedicine(
        medical_prescription_medicine_id=1,
        operation_type="Realização",
        performed_at=datetime_from_string("17/11/2022 22:15:00"),
    )

    new_history.medical_prescription_medicines.append(
        new_history_medical_prescription_medicine
    )

    new_history_medical_prescription_orientation = (
        HistoryMedicalPrescriptionOrientation(
            medical_prescription_orientation_id=1,
            operation_type="Realização",
            performed_at=datetime_from_string("17/11/2022 22:15:00"),
        )
    )

    new_history.medical_prescription_orientations.append(
        new_history_medical_prescription_orientation
    )

    new_history_medical_prescription_procedure = HistoryMedicalPrescriptionProcedure(
        medical_prescription_procedure_id=1,
        operation_type="Realização",
        performed_at=datetime_from_string("17/11/2022 22:15:00"),
    )

    new_history.medical_prescription_procedures.append(
        new_history_medical_prescription_procedure
    )

    db.session.add(new_history)

    new_history = History(admission_id=2, professional_id=2, type="Clínico")

    new_history_medical_prescription_medicine = HistoryMedicalPrescriptionMedicine(
        medical_prescription_medicine_id=2,
        operation_type="Realização",
        performed_at=datetime_from_string("15/09/2022 20:57:00"),
    )

    new_history.medical_prescription_medicines.append(
        new_history_medical_prescription_medicine
    )

    new_history_medical_prescription_orientation = (
        HistoryMedicalPrescriptionOrientation(
            medical_prescription_orientation_id=2,
            operation_type="Realização",
            performed_at=datetime_from_string("15/09/2022 20:57:00"),
        )
    )

    new_history.medical_prescription_orientations.append(
        new_history_medical_prescription_orientation
    )

    new_history_medical_prescription_procedure = HistoryMedicalPrescriptionProcedure(
        medical_prescription_procedure_id=2,
        operation_type="Realização",
        performed_at=datetime_from_string("15/09/2022 20:57:00"),
    )

    new_history.medical_prescription_procedures.append(
        new_history_medical_prescription_procedure
    )

    db.session.add(new_history)

    db.session.commit()
