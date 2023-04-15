from app.main import db
from app.main.exceptions import DefaultException
from app.main.model import CommissionType

COMMISSION_TYPES = [
    "ÉTICA MÉDICA",
    "ÉTICA DE ENFERMAGEM",
    "FARMÁCIA E TERAPÊUTICA",
    "CONTROLE DE INFECÇÃO HOSPITALAR",
    "APROPRIAÇÃO DE CUSTOS",
    "CIPA",
    "REVISÃO DE PRONTUÁRIOS",
    "REVISÃO DE DOCUMENTAÇÃO MÉDICA E ESTATÍSTICA",
    "ANÁLISE DE ÓBITOS E BIÓPSIAS",
    "INVESTIGAÇÃO EPIDEMIOLÓGICA",
    "NOTIFICAÇÃO DE DOENÇAS",
    "CONTROLE DE DOENÇAS",
    "CONTROLE DE ZOONOSES E VETORES",
    "MORTALIDADE MATERNA",
    "MORTALIDADE NEONATAL",
]


def get_commission_types(options: list = None):
    query = CommissionType.query

    if options is not None:
        query = query.options(*options)

    commission_types = query.all()
    return commission_types


def create_default_commission_types():
    for _commission_type in COMMISSION_TYPES:
        commission_type = CommissionType(name=_commission_type)
        db.session.add(commission_type)
    db.session.commit()


def get_commission_type(
    commission_type_id: int, options: list = None
) -> CommissionType:

    query = CommissionType.query

    if options is not None:
        query = query.options(*options)

    commission_type = query.get(commission_type_id)

    if commission_type is None:
        raise DefaultException("commission_type_not_found", code=404)

    return commission_type


def validate_commission_types(commission_types_ids: set[int]) -> list[CommissionType]:

    commission_types = CommissionType.query.filter(
        CommissionType.id.in_(commission_types_ids)
    ).all()

    commission_types_ids_db = set(
        commission_type.id for commission_type in commission_types
    )

    if commission_types_ids != commission_types_ids_db:
        raise DefaultException("commission_type_not_found", code=404)
    return commission_types
