from app.main.model import ItemClassification


def create_base_seed_item_classification(db):
    new_item_classification = ItemClassification(name="ITEM CLASSIFICATION ONE")

    db.session.add(new_item_classification)

    new_item_classification = ItemClassification(name="ITEM CLASSIFICATION TWO")

    db.session.add(new_item_classification)

    new_item_classification = ItemClassification(name="ITEM CLASSIFICATION THREE")

    db.session.add(new_item_classification)

    db.session.commit()
