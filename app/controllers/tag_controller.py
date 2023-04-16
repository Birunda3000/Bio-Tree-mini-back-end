from flask import request
from flask_restx import Namespace, Resource, fields
from service.tag_service import *

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

api = TagDto.api
tag_ns = api


@api.route("")
class Tag(Resource):
    @api.doc("list_tags",)
    @api.marshal_list_with(TagDto.tag_get, code=200, description="Get all tags")
    def get(self):
        """List all tags"""
        return get_all_tags()

    @api.doc("create_tag")
    @api.expect(TagDto.tag_post)
    def post(self):
        """Create a new tag"""
        data = request.json
        return save_new_tag(data=data)

@api.route("/<int:tag_id>")
class TagById(Resource):
    @api.doc("get_tag",)
    @api.marshal_with(TagDto.tag_get, code=200, description="Get tag by id")
    def get(self, tag_id):
        """Get tag by id"""
        return get_tag_by_id(tag_id)

    @api.doc("update_tag")
    @api.expect(TagDto.tag_post)
    def put(self, tag_id):
        """Update tag by id"""
        data = request.json
        return update_tag_by_id(tag_id, data=data)

    @api.doc("delete_tag")
    def delete(self, tag_id):
        """Delete tag by id"""
        return delete_tag_by_id(tag_id)
