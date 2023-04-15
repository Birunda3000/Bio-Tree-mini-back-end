from app.main.model import MedicalAppointment


def create_medical_appointment(db):
    new_medical_appointment = MedicalAppointment(
        patient_id=1,
        professional_id=1,
        description="Doente",
        diagnosis_type="Definitivo",
        diagnosis_work="Não",
        diagnosis_traffic_accident="Sim",
    )

    db.session.add(new_medical_appointment)

    new_medical_appointment = MedicalAppointment(
        patient_id=2,
        professional_id=2,
        description="Gripado",
        diagnosis_type="Provisório",
        diagnosis_work="Sim",
        diagnosis_traffic_accident="Não",
    )

    db.session.add(new_medical_appointment)
    db.session.commit()
