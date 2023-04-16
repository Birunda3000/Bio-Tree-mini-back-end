from flask import request
from flask_restx import Namespace, Resource, fields
from services.tag_service import *


class TagDto:
    api = Namespace("tag", description="tag related operations")

    tag_post = api.model(
        "tag_create",
        {
            "name": fields.String(required=True, description="tag name"),
            "description": fields.String(required=False, description="tag description"),
        },
    )

    tag_get = api.clone(
        "tag_get", tag_post, {"id": fields.Integer(required=True, description="tag id")}
    )
    tag_get_list = api.model(
        "tag_get_list",
        {
            "current_page": fields.Integer(required=True, description="current page"),
            "total_items": fields.Integer(required=True, description="total items"),
            "total_pages": fields.Integer(required=True, description="total pages"),
            "items": fields.List(fields.Nested(tag_get)),
        },
    )


api = TagDto.api
tag_ns = api


@api.route("")
class Tag(Resource):
    @api.doc(
        "list_tags",
        params={
            "page": "Page number",
            "per_page": "Items per page",
            "name": "Tag name",
            "description": "Tag description",
        },
        description="List all tags. {page} and {per_page} are optional. If not provided, the default values are 1 and 10 respectively. {name} and {description} are optional. If provided, the results will be filtered by the provided values.",
    )
    @api.marshal_with(TagDto.tag_get_list, code=200, description="Get all tags")
    def get(self):
        """List all tags"""
        params = request.args
        return get_tags(params=params)

    @api.doc("create_tag")
    @api.expect(TagDto.tag_post)
    @api.response(201, "Tag_successfully_created")
    @api.response(400, "Invalid_data")
    @api.response(409, "This_Tag_already_exists")
    def post(self):
        """Create a new tag"""
        data = request.json
        return save_new_tag(data=data)


@api.route("/<int:tag_id>")
class TagById(Resource):
    @api.doc(
        "get_tag",
    )
    @api.marshal_with(TagDto.tag_get, code=200, description="Get tag by id")
    @api.response(404, "Tag_not_found")
    def get(self, tag_id):
        """Get tag by id"""
        return get_tag(tag_id)

    @api.doc("update_tag")
    @api.expect(TagDto.tag_post)
    @api.response(200, "Tag_successfully_updated")
    @api.response(400, "Invalid_data")
    @api.response(404, "Tag_not_found")
    def put(self, tag_id):
        """Update tag by id"""
        data = request.json
        return update_tag_by_id(tag_id, data=data)

    @api.doc("delete_tag")
    @api.response(200, "Tag_successfully_deleted")
    @api.response(404, "Tag_not_found")
    def delete(self, tag_id):
        """Delete tag by id"""
        return delete_tag_by_id(tag_id)
