from app.main.model import Action


def create_base_seed_action(db):

    new_action = Action(name="AÇÃO TESTE 1")
    db.session.add(new_action)

    new_action = Action(name="AÇÃO TESTE 2")
    db.session.add(new_action)

    new_action = Action(name="AÇÃO TESTE 3")
    db.session.add(new_action)

    db.session.commit()
