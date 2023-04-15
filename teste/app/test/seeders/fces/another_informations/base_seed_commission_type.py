from app.main.model import CommissionType


def create_base_seed_commission_type(db):

    new_commission_type = CommissionType(name="ÉTICA MÉDICA")

    db.session.add(new_commission_type)

    new_commission_type = CommissionType(name="ÉTICA DE ENFERMAGEM")

    db.session.add(new_commission_type)

    new_commission_type = CommissionType(name="FARMÁCIA E TERAPÊUTICA")

    db.session.add(new_commission_type)

    new_commission_type = CommissionType(name="CONTROLE DE INFECÇÃO HOSPITALAR")

    db.session.add(new_commission_type)

    new_commission_type = CommissionType(name="APROPRIAÇÃO DE CUSTOS")

    db.session.add(new_commission_type)

    new_commission_type = CommissionType(name="CIPA")

    db.session.add(new_commission_type)

    new_commission_type = CommissionType(name="REVISÃO DE PRONTUÁRIOS")

    db.session.add(new_commission_type)

    new_commission_type = CommissionType(
        name="REVISÃO DE DOCUMENTAÇÃO MÉDICA E ESTATÍSTICA"
    )

    db.session.add(new_commission_type)

    new_commission_type = CommissionType(name="ANÁLISE DE ÓBITOS E BIÓPSIAS")

    db.session.add(new_commission_type)

    new_commission_type = CommissionType(name="INVESTIGAÇÃO EPIDEMIOLÓGICA")

    db.session.add(new_commission_type)

    new_commission_type = CommissionType(name="NOTIFICAÇÃO DE DOENÇAS")

    db.session.add(new_commission_type)

    new_commission_type = CommissionType(name="CONTROLE DE DOENÇAS")

    db.session.add(new_commission_type)

    new_commission_type = CommissionType(name="CONTROLE DE ZOONOSES E VETORES")

    db.session.add(new_commission_type)

    new_commission_type = CommissionType(name="MORTALIDADE MATERNA")

    db.session.add(new_commission_type)

    new_commission_type = CommissionType(name="MORTALIDADE NEONATAL")

    db.session.add(new_commission_type)

    db.session.commit()
