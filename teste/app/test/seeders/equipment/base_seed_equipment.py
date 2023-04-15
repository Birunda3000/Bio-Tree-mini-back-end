from app.main.model import Equipment, EquipmentType


def create_base_seed_equipment(db):
    equipment_type = EquipmentType.query.get(1)

    new_equipment = Equipment(name="EQUIPAMENTO TESTE 1", equipment_type=equipment_type)
    db.session.add(new_equipment)

    new_equipment = Equipment(name="EQUIPAMENTO TESTE 2", equipment_type=equipment_type)
    db.session.add(new_equipment)

    db.session.commit()
