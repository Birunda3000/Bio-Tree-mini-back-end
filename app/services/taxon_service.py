from math import ceil

from config import Config, db
from models import Taxon, Tag, TAXON_CLASS_TYPES
from responses import DefaultException, response
from werkzeug.datastructures import ImmutableMultiDict
from .tag_service import get_tag

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def get_taxons(params: ImmutableMultiDict) -> dict[str, any]:
    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)
    taxon_class = params.get("taxon_class", type=str)
    name = params.get("name", type=str)
    popular_name = params.get("popular_name", type=str)
    description = params.get("description", type=str)
    origin = params.get("origin", type=int)
    extinction = params.get("extinction", type=int)
    superior_taxon_id = params.get("superior_taxon_id", type=int)
    tag_id = params.get("tag_id", type=int)
    ancestor_id = params.get("ancestor_id", type=int)
    filters = []
    if taxon_class:
        filters.append(Taxon.taxon == taxon_class)
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
    if superior_taxon_id:
        filters.append(Taxon.superior_taxon.id == superior_taxon_id)
    if tag_id:
        filters.append(Taxon.tags.any(id=tag_id))
    if ancestor_id:
        filters.append(Taxon.ancestors.any(id=ancestor_id))

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
    verify_superior_taxon(
        taxon_class=data.get("taxon_class"),
        superior_taxon_id=data.get("superior_taxon"),
    )

    taxon = Taxon.query.filter_by(name=data["name"]).first()

    if taxon is not None:
        raise DefaultException(message="This_Taxon_already_exists", code=409)

    tags = []
    if "tags" in data:
        tag_ids = data["tags_ids"]
        tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    
    ancestors = []
    if "ancestors" in data:
        ancestor_ids = data["ancestors_ids"]
        ancestors = Taxon.query.filter(Taxon.id.in_(ancestor_ids)).all()

    new_taxon = Taxon(
        taxon_class=data.get("taxon_class"),
        name=data.get("name"),
        popular_name=data.get("popular_name"),
        description=data.get("description"),
        origin=data.get("origin"),
        extinction=data.get("extinction"),
        individuals_number=data.get("individuals_number"),
        superior_taxon=data.get("superior_taxon"),
        tags=tags,
        ancestors=ancestors,
    )
    db.session.add(new_taxon)
    db.session.commit()
    return response(status="success", message="Taxon_successfully_created", code=201)


def update_taxon_by_id(taxon_id, data) -> dict[str, any]:
    verify_superior_taxon(
        taxon_class=data.get("taxon_class"),
        superior_taxon_id=data.get("superior_taxon"),
    )
    taxon = get_taxon(taxon_id)

    if "tags" in data:
        tag_ids = data["tags_ids"]
        tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    
    if "ancestors" in data:
        ancestor_ids = data["ancestors_ids"]
        ancestors = Taxon.query.filter(Taxon.id.in_(ancestor_ids)).all()

    taxon.taxon_class = data.get("taxon_class")
    taxon.name = data.get("name")
    taxon.popular_name = data.get("popular_name")
    taxon.description = data.get("description")
    taxon.origin = data.get("origin")
    taxon.extinction = data.get("extinction")
    taxon.individuals_number = data.get("individuals_number")
    taxon.tags = tags
    taxon.ancestors = ancestors
    db.session.commit()
    return response(status="success", message="Taxon_successfully_updated", code=200)


def delete_taxon_by_id(taxon_id) -> dict[str, any]:
    taxon = Taxon.query.filter_by(id=taxon_id).first()
    if taxon is None:
        raise DefaultException(message="Taxon_does_not_exist.", code=404)
    db.session.delete(taxon)
    db.session.commit()
    return response(status="success", message="Taxon_successfully_deleted", code=200)


def verify_superior_taxon(taxon_class: str, superior_taxon_id: Taxon) -> bool:
    """Verify if the superior taxon is valid"""
    if taxon_class == "life" and superior_taxon_id is None:
        return True
    elif taxon_class == "life" and superior_taxon_id is not None:
        raise DefaultException(message="Life_does_not_have_superior_taxon", code=400)

    if superior_taxon_id is None:
        return True

    superior_taxon = get_taxon(superior_taxon_id)

    if TAXON_CLASS_TYPES.index(taxon_class) - 1 != TAXON_CLASS_TYPES.index(
        superior_taxon.taxon_class
    ):
        raise DefaultException(
            message="Taxon_{}_is_not_a_valid_superior_taxon_of_{},_it_should_be_a_{}".format(
                superior_taxon.name,
                taxon_class,
                TAXON_CLASS_TYPES[TAXON_CLASS_TYPES.index(taxon_class) - 1],
            ),
            code=400,
        )
    return True

def verify_ancestor_taxon(taxon: Taxon, ancestors_taxons_id: list) -> bool:
    """Verify if an list of taxons can be ancestors of a taxon"""
    

    
