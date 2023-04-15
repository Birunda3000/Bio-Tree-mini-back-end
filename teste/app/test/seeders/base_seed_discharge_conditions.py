from app.main.model import DischargeCondition


def create_base_seed_discharge_conditions(db):
    """Add 2 DischargeConditions"""

    new_discharge_condition = DischargeCondition(name="Discharge condition teste 1")

    new_discharge_condition2 = DischargeCondition(name="Discharge condition teste 2")

    new_discharge_condition3 = DischargeCondition(name="Discharge condition teste 3")

    db.session.add(new_discharge_condition)
    db.session.add(new_discharge_condition2)
    db.session.add(new_discharge_condition3)
    db.session.commit()
