from app.main.model import ContractRule


def create_base_seed_contract_rule(db):
    contract_rule = ContractRule(
        code="00.01",
        description="regra contratual teste 1",
        ordinance="teste",
        type="CENTRALIZADA",
    )
    db.session.add(contract_rule)

    contract_rule = ContractRule(
        code="00.02",
        description="regra contratual teste 2",
        ordinance="teste",
        type="DESCENTRALIZADA",
    )
    db.session.add(contract_rule)

    db.session.commit()
