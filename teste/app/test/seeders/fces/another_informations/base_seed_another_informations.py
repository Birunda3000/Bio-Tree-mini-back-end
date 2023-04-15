from app.main.model import AnotherInformations, CommissionType, Fces, Leavings
from app.main.service import date_from_string


def create_base_seed_another_informations(db):

    fces = Fces.query.get(1)
    commission_type = CommissionType.query.get(1)
    leavings = Leavings.query.get(1)

    new_another_informations = AnotherInformations(
        fces=fces,
        sanitary_number="54321",
        issuance_date=date_from_string("29/09/2020"),
        issuing_agency="SES",
        bank="249",
        agency="6491",
        current_account="619949",
        administrative_field="Federal",
        hierarchy_level="Nível de hierarquia",
        teaching_research_activity_text="Hospital Universitário",
        tax_withholding="IRPJ",
        service_shift="Noite",
        nature_organization="Empresa",
        attendance="Atendimento",
        covenant="Público",
        commission_types_selected=[commission_type],
        leavings_selected=[leavings],
    )

    db.session.add(new_another_informations)

    fces = Fces.query.get(2)
    commission_type = CommissionType.query.get(1)
    leavings = Leavings.query.get(1)

    new_another_informations = AnotherInformations(
        fces=fces,
        sanitary_number="12345",
        issuance_date=date_from_string("09/09/2022"),
        issuing_agency="SES",
        bank="543",
        agency="9872",
        current_account="435765",
        administrative_field="Estadual",
        hierarchy_level="Nível de hierarquia",
        tax_withholding="CSLL",
        service_shift="Manhã",
        nature_organization="Cooperativa",
        attendance="Atendimento",
        covenant="Privado",
        commission_types_selected=[commission_type],
        leavings_selected=[leavings],
    )

    db.session.add(new_another_informations)

    db.session.commit()
