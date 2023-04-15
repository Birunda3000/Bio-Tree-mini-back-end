from json import loads
from math import ceil

from sqlalchemy import and_, or_
from werkzeug.datastructures import ImmutableMultiDict

from app.main import db
from app.main.config import Config
from app.main.exceptions import DefaultException
from app.main.model import Supplier

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def get_suppliers(params: ImmutableMultiDict):

    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)
    name = params.get("name", type=str)
    cpf = params.get("cpf", type=str)
    cnpj = params.get("cnpj", type=str)
    legal_person = params.get("legal_person", type=str)
    legal_person = loads(legal_person) if legal_person else None

    filters = []

    if name:
        filters.append(Supplier.name.ilike(f"%{name.upper()}%"))
    if cpf:
        filters.append(Supplier.cpf.ilike(f"%{cpf.upper()}%"))
    if cnpj:
        filters.append(Supplier.cnpj.ilike(f"%{cnpj.upper()}%"))
    if legal_person == True:
        filters.append(Supplier.cnpj != None)
    elif legal_person == False:
        filters.append(Supplier.cpf != None)

    pagination = (
        Supplier.query.filter(*filters)
        .order_by(Supplier.id)
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return {
        "current_page": page,
        "total_items": pagination.total,
        "total_pages": ceil(pagination.total / per_page),
        "items": pagination.items,
    }


def save_new_supplier(data: dict[str, any]) -> None:

    name = data.get("name").upper()
    cpf = data.get("cpf")
    cnpj = data.get("cnpj")

    _supplier_exists(name=name, cpf=cpf, cnpj=cnpj)

    _cpf_or_cnpj_exists(cpf=cpf, cnpj=cnpj)

    new_supplier = Supplier(name=name, cpf=cpf, cnpj=cnpj)

    db.session.add(new_supplier)
    db.session.commit()


def update_supplier(supplier_id: int, data: dict[str, str]) -> None:

    supplier = get_supplier(supplier_id=supplier_id)

    new_name = data.get("name").upper()

    if supplier.name != new_name:

        _supplier_exists(name=new_name, cpf=supplier.cpf, cnpj=supplier.cnpj)

        supplier.name = new_name

        db.session.commit()


def delete_supplier(supplier_id: int):

    supplier = get_supplier(supplier_id=supplier_id)

    db.session.delete(supplier)
    db.session.commit()


def get_supplier(supplier_id: int, options: list = None) -> Supplier:

    query = Supplier.query

    if options is not None:
        query = query.options(*options)

    supplier = query.get(supplier_id)

    if supplier is None:
        raise DefaultException("supplier_not_found", code=404)

    return supplier


def _supplier_exists(name: str, cpf: str, cnpj: str) -> bool:

    filters = [Supplier.name == name.upper()]
    if cpf:
        filters.append(Supplier.cpf != None)
    elif cnpj:
        filters.append(Supplier.cnpj != None)

    if Supplier.query.with_entities(Supplier.id).filter(*filters).scalar() is not None:
        raise DefaultException("name_in_use", code=409)


def _cpf_or_cnpj_exists(cpf: str, cnpj: str):
    filters = [
        or_(
            and_(Supplier.cpf == cpf, Supplier.cpf != None),
            and_(Supplier.cnpj == cnpj, Supplier.cnpj != None),
        )
    ]

    if (
        supplier := Supplier.query.with_entities(Supplier.cpf, Supplier.cnpj)
        .filter(*filters)
        .first()
    ):
        if (cpf is not None) and (supplier.cpf == cpf):
            raise DefaultException("cpf_in_use", code=409)
        elif (cnpj is not None) and (supplier.cnpj == cnpj):
            raise DefaultException("cnpj_in_use", code=409)
