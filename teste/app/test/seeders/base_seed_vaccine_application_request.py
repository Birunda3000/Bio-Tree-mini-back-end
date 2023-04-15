from app.main.model import VaccineApplicationRequest


def create_base_seed_vaccine_application_request(db):

    new_vaccine_application_request = VaccineApplicationRequest(
        professional_id=1,
        patient_id=1,
        vaccine_id=1,
    )
    db.session.add(new_vaccine_application_request)

    new_vaccine_application_request = VaccineApplicationRequest(
        professional_id=1, patient_id=2, vaccine_id=1, status="Cancelada"
    )
    db.session.add(new_vaccine_application_request)

    db.session.commit()
