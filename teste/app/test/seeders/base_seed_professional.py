from app.main.model.address_model import Address
from app.main.model.professional_model import Professional
from app.main.service import date_from_string


def create_base_seed_professional(db):
    """Add 2 Professionals"""

    new_address = Address(
        street="Rua Domingos Olímpio",
        district="Centro",
        city="Sobral",
        state="CE",
        complement="Proximo ao supermercado",
        number="900",
        cep="62011140",
    )

    new_professional = Professional(
        name="Profissional teste 1",
        social_name="Profissional teste 1 nome social",
        email="profissional1@uece.com",
        cpf="11545559090",
        birth=date_from_string("24/08/1989"),
        sex="Masculino",
        mother_name="Mãe profissional teste 1",
        father_name="Pai profissional teste 1",
        cns_cod="867771826050006",
        address=new_address,
    )

    db.session.add(new_professional)

    new_address = Address(
        street="Rua São Damião",
        district="Presidente Kennedy",
        city="Fortaleza",
        state="CE",
        complement="Proximo a farmacia",
        number="871",
        cep="60355265",
    )

    new_professional = Professional(
        name="Profissional teste 2",
        social_name="Profissional teste 2 nome social",
        email="profissional2@uece.com",
        cpf="10177488026",
        birth=date_from_string("22/11/1979"),
        sex="Feminino",
        mother_name="Mãe profissional teste 2",
        father_name="Pai profissional teste 2",
        cns_cod="181915807040001",
        address=new_address,
    )

    db.session.add(new_professional)

    new_address = Address(
        street="Rua Cedro",
        district="Jorge Teixeira",
        city="Ji-Paraná",
        state="RO",
        complement="Proximo ao mercado",
        number="900",
        cep="76912840",
    )

    new_professional = Professional(
        name="Profissional teste 3",
        social_name="Profissional teste 3 nome social",
        email="profissional3@uece.com",
        cpf="68071661090",
        birth=date_from_string("29/08/1990"),
        sex="Feminino",
        mother_name="Mãe profissional teste 3",
        father_name="Pai profissional teste 3",
        cns_cod="181915807040115",
        address=new_address,
    )

    db.session.add(new_professional)
    db.session.commit()
