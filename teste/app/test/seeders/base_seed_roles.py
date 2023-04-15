from app.main.model import Resource, Role


def create_base_seed_role(db):
    """Add 2 roles"""

    new_role = Role(
        name="Secretária",
        resources=[Resource.query.filter(Resource.code == "atendimento").first()],
    )

    db.session.add(new_role)

    new_role = Role(
        name="Enfermeira",
        resources=Resource.query.filter(
            (Resource.code == "atendimento")
            | (Resource.code == "gerenciamentodepaciente")
        ).all(),
    )

    db.session.add(new_role)
    db.session.commit()
