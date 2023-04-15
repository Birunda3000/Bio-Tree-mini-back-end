from app.main.model import Room


def create_base_seed_room(db):
    """Add 3 rooms"""

    new_room = Room(name="Sala Teste 1")
    db.session.add(new_room)

    new_room = Room(name="Sala Teste 2")
    db.session.add(new_room)

    new_room = Room(name="Sala Teste 3")
    db.session.add(new_room)

    db.session.commit()
