from math import ceil

from config import Config, db
from models import Taxon, Tag
from responses import DefaultException, response
from werkzeug.datastructures import ImmutableMultiDict
from .tag_service import get_tag

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def get_taxons(params: ImmutableMultiDict) -> dict[str, any]:
    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)
    taxon = params.get("taxon", type=str)
    name = params.get("name", type=str)
    popular_name = params.get("popular_name", type=str)
    description = params.get("description", type=str)
    origin = params.get("origin", type=int)
    extinction = params.get("extinction", type=int)
    filters = []
    if name:
        filters.append(Taxon.name.ilike(f"%{name}%"))
    if popular_name:
        filters.append(Taxon.popular_name.ilike(f"%{popular_name}%"))
    if description:
        filters.append(Taxon.description.ilike(f"%{description}%"))
    if origin:
        filters.append(Taxon.origin == origin)
    if extinction:
        filters.append(Taxon.extinction == extinction)

    pagination = (
        Taxon.query.filter(*filters)
        .order_by(Taxon.id)
        .paginate(page=page, per_page=per_page, error_out=False)
    )
    return {
        "current_page": page,
        "total_items": pagination.total,
        "total_pages": ceil(pagination.total / per_page),
        "items": pagination.items,
    }


def get_taxon(taxon_id: int, options: list = None) -> Taxon:
    """Get a taxon"""
    if options is None:
        options = []
    taxon = Taxon.query.options(*options).filter_by(id=taxon_id).first()
    if taxon is None:
        raise DefaultException(message="Taxon_not_found", code=404)
    return taxon


def save_new_taxon(data: dict[str, any]) -> dict[str, any]:
    taxon = Taxon.query.filter_by(name=data["name"]).first()

    if taxon is not None:
        raise DefaultException(message="This_Taxon_already_exists", code=409)

    tags = []
    if "tags" in data:
        tag_ids = data["tags"]
        tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_taxon = Taxon(
        taxon=data.get("taxon"),
        name=data.get("name"),
        popular_name=data.get("popular_name"),
        description=data.get("description"),
        origin=data.get("origin"),
        extinction=data.get("extinction"),
        individuals_number=data.get("individuals_number"),
        tags=tags,
    )
    db.session.add(new_taxon)
    db.session.commit()
    return response(status="success", message="Taxon_successfully_created", code=201)


def update_taxon_by_id(taxon_id, data) -> dict[str, any]:
    taxon = Taxon.query.filter_by(id=taxon_id).first()
    if taxon is None:
        raise DefaultException(message="Taxon_does_not_exist", code=404)
    
    tags = []
    if "tags" in data:
        tag_ids = data["tags"]
        tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    taxon.taxon = data.get("taxon")
    taxon.name = data.get("name")
    taxon.popular_name = data.get("popular_name")
    taxon.description = data.get("description")
    taxon.origin = data.get("origin")
    taxon.extinction = data.get("extinction")
    taxon.individuals_number = data.get("individuals_number")
    taxon.tags = tags
    db.session.commit()
    return response(status="success", message="Taxon_successfully_updated", code=200)


def delete_taxon_by_id(taxon_id) -> dict[str, any]:
    taxon = Taxon.query.filter_by(id=taxon_id).first()
    if taxon is None:
        raise DefaultException(message="Taxon_does_not_exist.", code=404)
    db.session.delete(taxon)
    db.session.commit()
    return response(status="success", message="Taxon_successfully_deleted", code=200)
