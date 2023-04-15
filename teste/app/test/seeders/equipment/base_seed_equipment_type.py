from app.main.model import EquipmentType


def create_base_seed_equipment_type(db):
    new_equipment_type = EquipmentType(name="TIPO DE EQUIPAMENTO TESTE 1")
    db.session.add(new_equipment_type)

    new_equipment_type = EquipmentType(name="TIPO DE EQUIPAMENTO TESTE 2")
    db.session.add(new_equipment_type)

    db.session.commit()
