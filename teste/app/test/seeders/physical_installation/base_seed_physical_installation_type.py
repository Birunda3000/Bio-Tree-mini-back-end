from app.main.model import PhysicalInstallationType


def create_base_seed_physical_installation_type(db):

    new_physical_installation_type = PhysicalInstallationType(
        name="TIPO DE INSTALAÇÃO FÍSICA TESTE 1"
    )
    db.session.add(new_physical_installation_type)

    new_physical_installation_type = PhysicalInstallationType(
        name="TIPO DE INSTALAÇÃO FÍSICA TESTE 2"
    )
    db.session.add(new_physical_installation_type)

    db.session.commit()
