from app.main.model import VaccineApplication
from app.main.service import date_from_string


def create_base_seed_vaccine_application(db):

    new_vaccine_application = VaccineApplication(
        professional_id=1,
        patient_id=1,
        vaccine_name="BCG",
        application_type="Aplicação",
        manufacturer="F.A.P. - FUNDACAO ATAULPHO DE PAIVA",
        batch="1x4654",
        administration_route="Oral",
        application_site="Rede venosa",
        pregnancy_type="Não se aplica",
        performed_at=date_from_string("07/01/2023"),
    )
    db.session.add(new_vaccine_application)

    new_vaccine_application = VaccineApplication(
        professional_id=2,
        patient_id=2,
        vaccine_name="Hepatite B",
        application_type="Resgate",
        manufacturer="F.A.P. - FUNDACAO ATAULPHO DE PAIVA",
        batch="1x8795",
        administration_route="Subcutânea",
        application_site="Deltóide direito",
        pregnancy_type="Não se aplica",
        complement="Documento",
        performed_at=date_from_string("25/12/2022"),
    )
    db.session.add(new_vaccine_application)

    new_vaccine_application = VaccineApplication(
        professional_id=3,
        patient_id=3,
        edited=True,
        vaccine_name="Hepatite B",
        application_type="Aplicação",
        manufacturer="F.A.P. - FUNDACAO ATAULPHO DE PAIVA",
        batch="1x8795",
        administration_route="Subcutânea",
        application_site="Deltóide direito",
        pregnancy_type="Não se aplica",
        performed_at=date_from_string("22/11/2019"),
    )
    db.session.add(new_vaccine_application)

    new_vaccine_application = VaccineApplication(
        professional_id=4,
        patient_id=4,
        vaccine_name="Hepatite B",
        application_type="Aplicação",
        manufacturer="F.A.P. - FUNDACAO ATAULPHO DE PAIVA",
        batch="1x3972",
        administration_route="Oral",
        application_site="Deltóide direito",
        pregnancy_type="Não se aplica",
        performed_at=date_from_string("27/01/2022"),
    )
    db.session.add(new_vaccine_application)

    new_vaccine_application = VaccineApplication(
        professional_id=5,
        patient_id=5,
        deleted=True,
        vaccine_name="Antitetânica",
        application_type="Aplicação",
        manufacturer="F.A.P. - FUNDACAO ATAULPHO DE PAIVA",
        batch="1x4784",
        administration_route="Subcutânea",
        application_site="Deltóide esquerdo",
        pregnancy_type="Não se aplica",
        performed_at=date_from_string("12/07/2014"),
    )
    db.session.add(new_vaccine_application)

    db.session.commit()
