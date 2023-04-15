from app.main.model import ItemGroup


def create_base_seed_item_group(db):

    item_group = ItemGroup(name="ITEM GROUP 1")
    db.session.add(item_group)

    item_group = ItemGroup(name="ITEM GROUP 2")
    db.session.add(item_group)

    item_group = ItemGroup(name="ITEM GROUP 3")
    db.session.add(item_group)

    db.session.commit()
