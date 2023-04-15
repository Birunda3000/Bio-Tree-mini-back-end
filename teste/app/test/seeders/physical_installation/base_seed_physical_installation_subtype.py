from app.main.model import PhysicalInstallationSubtype, PhysicalInstallationType


def create_base_seed_physical_installation_subtype(db):

    new_physical_installation_subtype = PhysicalInstallationSubtype(
        name="SUBTIPO DE INSTALAÇÃO FÍSICA TESTE 1",
    )
    db.session.add(new_physical_installation_subtype)

    new_physical_installation_subtype = PhysicalInstallationSubtype(
        name="SUBTIPO DE INSTALAÇÃO FÍSICA TESTE 2",
    )
    db.session.add(new_physical_installation_subtype)

    db.session.commit()
