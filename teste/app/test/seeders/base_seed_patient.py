from app.main.model import Address, Contact, Patient
from app.main.service import date_from_string


def create_base_seed_patient(db):
    """Add 7 Patients"""

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
        cellphone="85987654321",
        emergency_contact="85998715975",
    )

    new_patient = Patient(
        name="Patient teste 1",
        social_name="Patient social name 1",
        cpf="11545559090",
        email="patient@test.com",
        birth=date_from_string("24/08/1989"),
        sex="Masculino",
        mother_name="Mãe patient teste 1",
        father_name="Pai patient teste 1",
        cns_cod="867771826050006",
        gender="HOMEM CIS",
        medical_number=1,
        breed="BRANCO",
        address=new_address,
        contact=new_contact,
    )

    db.session.add(new_patient)

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
        cellphone="85993897427",
        emergency_contact="5532243032",
    )

    new_patient = Patient(
        name="Patient teste 2",
        social_name="Patient social name 2",
        cpf="10177488026",
        email="patient2@test.com",
        birth=date_from_string("22/11/1979"),
        sex="Feminino",
        mother_name="Mãe patient teste 2",
        father_name="Pai patient teste 2",
        cns_cod="181915807040001",
        gender="MULHER CIS",
        medical_number=2,
        breed="PRETO",
        address=new_address,
        contact=new_contact,
    )

    db.session.add(new_patient)

    new_address = Address(
        street="Rua Travessa Alexandre",
        district="Siqueira",
        city="Fortaleza",
        state="CE",
        complement="Proximo ao extra",
        number="481",
        cep="60731-805",
    )

    new_contact = Contact(
        phone="8528736879",
        cellphone="85981049542",
        emergency_contact="8528736879",
    )

    new_patient = Patient(
        name="Patient teste 3",
        social_name="Patient social name 3",
        cpf="08678745380",
        email="patient3@test.com",
        birth=date_from_string("17/05/1997"),
        sex="Outros",
        mother_name="Mãe patient teste 3",
        father_name="Pai patient teste 3",
        cns_cod="298623574050001",
        gender="NÃO-BINÁRIO",
        medical_number=3,
        breed="PARDO",
        address=new_address,
        contact=new_contact,
    )

    db.session.add(new_patient)

    new_contact = Contact(
        cellphone="85993897427",
        emergency_contact="8538326822",
    )

    new_patient = Patient(
        name="Patient teste 4",
        social_name="Patient social name 4",
        cpf="18233703303",
        email="patient4@test.com",
        birth=date_from_string("06/07/1997"),
        sex="Masculino",
        mother_name="Mãe patient teste 4",
        father_name="Pai patient teste 4",
        cns_cod="177067460870018",
        gender="HOMEM TRANS",
        medical_number=4,
        breed="BRANCO",
        address=new_address,
        contact=new_contact,
    )

    db.session.add(new_patient)

    new_contact = Contact(
        cellphone="85993897427",
        emergency_contact="8538326822",
    )

    new_patient = Patient(
        name="Patient teste 5",
        social_name="Patient social name 5",
        cpf="19304165393",
        email="patient5@test.com",
        birth=date_from_string("16/02/1995"),
        sex="Feminino",
        mother_name="Mãe patient teste 5",
        father_name="Pai patient teste 5",
        cns_cod="850596135540001",
        gender="MULHER CIS",
        medical_number=5,
        breed="PRETO",
        address=new_address,
        contact=new_contact,
    )

    db.session.add(new_patient)

    new_contact = Contact(
        cellphone="85993897427",
        emergency_contact="5532243032",
    )

    new_patient = Patient(
        name="Patient teste 6",
        social_name="Patient social name 6",
        cpf="10885044002",
        email="patient6@test.com",
        birth=date_from_string("20/12/1991"),
        sex="Feminino",
        mother_name="Mãe patient teste 6",
        father_name="Pai patient teste 6",
        cns_cod="707314983320007",
        gender="MULHER TRANS",
        medical_number=6,
        breed="PRETO",
        address=new_address,
        contact=new_contact,
    )

    db.session.add(new_patient)

    new_contact = Contact(
        cellphone="85993897427",
        emergency_contact="5532243032",
    )

    new_patient = Patient(
        name="Patient teste 7",
        social_name="Patient social name 7",
        cpf="33463375028",
        email="patient7@test.com",
        birth=date_from_string("20/12/1991"),
        sex="Feminino",
        mother_name="Mãe patient teste 7",
        father_name="Pai patient teste 7",
        cns_cod="219123916900008",
        gender="MULHER CIS",
        medical_number=7,
        breed="BRANCO",
        address=new_address,
        contact=new_contact,
    )

    db.session.add(new_patient)

    new_contact = Contact(
        cellphone="85993897427",
        emergency_contact="5532243032",
    )

    new_patient = Patient(
        name="Patient teste 8",
        social_name="Patient social name 8",
        cpf="41942832010",
        email="patient8@test.com",
        birth=date_from_string("20/12/1991"),
        sex="Feminino",
        mother_name="Mãe patient teste 8",
        father_name="Pai patient teste 8",
        cns_cod="219123916900008",
        gender="MULHER CIS",
        medical_number=8,
        breed="BRANCO",
        address=new_address,
        contact=new_contact,
    )

    db.session.add(new_patient)

    new_contact = Contact(
        cellphone="85973679647",
        emergency_contact="5534676428",
    )

    new_patient = Patient(
        name="Patient teste 9",
        social_name="Patient social name 9",
        cpf="93409303049",
        email="patient9@test.com",
        birth=date_from_string("25/04/1989"),
        sex="Feminino",
        mother_name="Mãe patient teste 9",
        father_name="Pai patient teste 9",
        cns_cod="859086021630018",
        gender="MULHER CIS",
        medical_number=9,
        breed="BRANCO",
        address=new_address,
        contact=new_contact,
    )

    db.session.add(new_patient)

    new_contact = Contact(
        cellphone="85957476587",
        emergency_contact="8534789647",
    )

    new_patient = Patient(
        name="Patient teste 10",
        social_name="Patient social name 10",
        cpf="76833726094",
        email="patient10@test.com",
        birth=date_from_string("14/07/1994"),
        sex="Masculino",
        mother_name="Mãe patient teste 10",
        father_name="Pai patient teste 10",
        cns_cod="710176196590007",
        gender="HOMEM CIS",
        medical_number=10,
        breed="BRANCO",
        address=new_address,
        contact=new_contact,
    )

    db.session.add(new_patient)

    new_contact = Contact(
        cellphone="85957476587",
        emergency_contact="8534789647",
    )

    new_patient = Patient(
        name="Patient teste 11",
        social_name="Patient social name 11",
        cpf="96316543034",
        email="patient11@test.com",
        birth=date_from_string("27/05/1987"),
        sex="Feminino",
        mother_name="Mãe patient teste 11",
        father_name="Pai patient teste 11",
        cns_cod="839731439610002",
        gender="MULHER CIS",
        medical_number=11,
        breed="BRANCO",
        address=new_address,
        contact=new_contact,
    )

    db.session.add(new_patient)

    db.session.commit()
