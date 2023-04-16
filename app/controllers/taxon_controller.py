from flask import request
from flask_restx import Namespace, Resource, fields
from models import TAXON_TYPES
from services.taxon_service import *
from controllers.tag_controller import TagDto


class TaxonDto:
    api = Namespace("taxon", description="taxon related operations")

    taxon_post = api.model(
        "taxon_create",
        {
            "taxon": fields.String(
                required=True, description="taxon name", enum=TAXON_TYPES
            ),
            "name": fields.String(required=True, description="taxon name"),
            "popular_name": fields.String(
                required=False, description="taxon popular name"
            ),
            "description": fields.String(
                required=False, description="taxon description"
            ),
            "origin": fields.String(required=False, description="taxon origin"),
            "extinction": fields.String(required=False, description="taxon extinction"),
            "individuals_number": fields.Integer(
                required=False, description="taxon individuals number"
            ),
            "tags_id" : fields.List(
                fields.Integer(required=True, description="tag id"),
                required=False,
                description="tag ids",
            ),
        },
    )

    Tags = {
        "tags": fields.List(fields.Nested(TagDto.tag_get)),
    }

    taxon_get = api.clone(
        "taxon_get",
        taxon_post,
        Tags,
        {"id": fields.Integer(required=True, description="taxon id")},
    )

    taxon_get_list = api.model(
        "taxon_get_list",
        {
            "current_page": fields.Integer(required=True, description="current page"),
            "total_items": fields.Integer(required=True, description="total items"),
            "total_pages": fields.Integer(required=True, description="total pages"),
            "items": fields.List(fields.Nested(taxon_get)),
        },
    )


api = TaxonDto.api
taxon_ns = api


@api.route("")
class Taxon(Resource):
    @api.doc(
        "list_taxons",
        params={
            "page": "Page number",
            "per_page": "Items per page",
            "taxon": "Taxon name",
            "name": "Taxon name",
            "popular_name": "Taxon popular name",
            "description": "Taxon description",
            "origin": "Taxon origin",
            "extinction": "Taxon extinction",
        },
        description="List all taxons. {page} and {per_page} are optional. If not provided, the default values are 1 and 10 respectively. {name} and {description} are optional. If provided, the results will be filtered by the provided values.",
    )
    @api.marshal_with(TaxonDto.taxon_get_list, code=200, description="Get all taxons")
    def get(self):
        """List all taxons"""
        params = request.args
        return get_taxons(params=params)

    @api.doc("create_taxon")
    @api.expect(TaxonDto.taxon_post)
    @api.response(201, "Taxon_successfully_created")
    @api.response(400, "Invalid_data")
    @api.response(409, "This_Taxon_already_exists")
    def post(self):
        """Create a new taxon"""
        data = request.json
        return save_new_taxon(data=data)


@api.route("/<int:taxon_id>")
class TaxonById(Resource):
    @api.doc("get_taxon")
    @api.marshal_with(TaxonDto.taxon_get, code=200, description="Get taxon")
    def get(self, taxon_id):
        """Get taxon by id"""
        return get_taxon(taxon_id=taxon_id)

    @api.doc("update_taxon")
    @api.expect(TaxonDto.taxon_post)
    @api.response(200, "Taxon_successfully_updated")
    @api.response(400, "Invalid_data")
    @api.response(404, "Taxon_not_found")
    def put(self, taxon_id):
        """Update taxon by id"""
        data = request.json
        return update_taxon_by_id(taxon_id=taxon_id, data=data)

    @api.doc("delete_taxon")
    @api.response(200, "Taxon_successfully_deleted")
    @api.response(404, "Taxon_not_found")
    def delete(self, taxon_id):
        """Delete taxon by id"""
        return delete_taxon_by_id(taxon_id=taxon_id)
