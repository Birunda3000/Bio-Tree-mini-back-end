from app.main.model import CompanyAddress, Contact, Fces


def create_base_seed_fces(db):
    """Add 2 Fces"""

    new_address = CompanyAddress(
        sanitary_district_id=1,
        street="Rua São Damião",
        district="Presidente Kennedy",
        city="Fortaleza",
        state="CE",
        complement="Proximo a farmacia",
        number="871",
        cep="60355265",
        municipality="Fortaleza",
        latitude=3.727380,
        longitude=38.570772,
        regional_health="Regional III ",
        microregion="Metropolitana de Fortaleza",
        assistance_module="Módulo de assistência",
    )

    new_contact = Contact(
        phone="8532165498",
        fax="558530352020",
    )

    new_fces = Fces(
        maintainer_id=1,
        professional_id=1,
        corporate_name="Estabelecimento Teste 1",
        commercial_name="Estabelecimento teste 1",
        cnes_code=15866318,
        person_type="Jurídica",
        cnpj="80280198000143",
        email="string@example.br",
        establishment_code=215486,
        situation="Individual",
        establishment_type="Tipo de estabelecimento",
        establishment_subtype="Subtipo de estabelecimento",
        regulatory_registration_end_date="Data de término do registro regulamentar",
        payment_to_provider="Fixo",
        company_address=new_address,
        contact=new_contact,
    )
    db.session.add(new_fces)

    new_address = CompanyAddress(
        sanitary_district_id=1,
        street="Rua Domingos Olímpio",
        district="Centro",
        city="Sobral",
        state="CE",
        complement="Proximo ao supermercado",
        number="900",
        cep="62011140",
        municipality="Sobral",
        latitude=-3.727380,
        longitude=-38.570772,
        regional_health="Regional III ",
        microregion="Metropolitana de Fortaleza",
        assistance_module="Módulo de assistência",
    )

    new_contact = Contact(
        phone="8532165498",
        fax="558530352020",
    )

    new_fces = Fces(
        maintainer_id=1,
        professional_id=1,
        corporate_name="Estabelecimento Teste 2",
        commercial_name="Estabelecimento teste 2",
        cnes_code=1598625,
        person_type="Física",
        cpf="14525323892",
        email="string2@example.br",
        establishment_code=356884,
        situation="Mantido",
        establishment_type="Tipo de estabelecimento",
        establishment_subtype="Subtipo de estabelecimento",
        regulatory_registration_end_date="Data de término do registro regulamentar",
        payment_to_provider="Produção",
        company_address=new_address,
        contact=new_contact,
    )
    db.session.add(new_fces)

    new_address = CompanyAddress(
        sanitary_district_id=1,
        street="Rua Dezesseis de Janeiro",
        district="Autran Nunes",
        city="Fortaleza",
        state="CE",
        complement="Proximo a Padaria Que Sabor",
        number="545",
        cep="60526360",
        municipality="Fortaleza",
        latitude=-3.727380,
        longitude=-38.570772,
        regional_health="Regional III ",
        microregion="Metropolitana de Fortaleza",
        assistance_module="Módulo de assistência",
    )

    new_contact = Contact(
        phone="8534861592",
        fax="687154351998",
    )

    new_fces = Fces(
        maintainer_id=1,
        professional_id=1,
        corporate_name="Estabelecimento Teste 3",
        commercial_name="Estabelecimento teste 3",
        cnes_code=1698698,
        person_type="Física",
        cpf="30784058008",
        email="string3@example.br",
        establishment_code=986245,
        situation="Mantido",
        establishment_type="Tipo de estabelecimento",
        establishment_subtype="Subtipo de estabelecimento",
        regulatory_registration_end_date="Data de término do registro regulamentar",
        payment_to_provider="Produção",
        company_address=new_address,
        contact=new_contact,
    )
    db.session.add(new_fces)

    db.session.commit()
