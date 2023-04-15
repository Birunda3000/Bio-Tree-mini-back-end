from app.main.model import Address, Contact, Maintainer


def create_base_seed_maintainer(db):
    """Add 2 Maintainers"""

    new_address = Address(
        street="Rua São Damião",
        district="Presidente Kennedy",
        city="Fortaleza",
        state="CE",
        complement="Proximo a farmacia",
        number="871",
        cep="60355265",
    )

    new_contact = Contact(
        phone="8533165440",
        fax="551130354050",
    )

    new_maintainer = Maintainer(
        corporate_name="Hospital Central Teste 1",
        commercial_name="Hospital Central Teste",
        cnpj="02569021000158",
        regional_number=11,
        unit_type="Privada",
        email="maintaniner1@test.com",
        address=new_address,
        contact=new_contact,
    )

    db.session.add(new_maintainer)

    new_address = Address(
        street="Rua Domingos Olímpio",
        district="Centro",
        city="Sobral",
        state="CE",
        complement="Proximo ao supermercado",
        number="900",
        cep="62011140",
    )

    new_contact = Contact(
        phone="8532165498",
        fax="551130352020",
    )

    new_maintainer = Maintainer(
        corporate_name="Hospital Teste 1",
        commercial_name="Hospital Teste",
        cnpj="00623904000173",
        regional_number=5,
        unit_type="Pública",
        email="maintaniner2@test.com",
        address=new_address,
        contact=new_contact,
    )

    db.session.add(new_maintainer)

    db.session.commit()
