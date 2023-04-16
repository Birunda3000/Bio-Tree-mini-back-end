#from app.service.tag_service import * # ImportError: cannot import name 'tag_ns' from partially initialized module 'controllers' (most likely due to a circular import) (C:\Users\esdn6\Documents\GitHub\Bio-Tree-mini-back-end\app\controllers\__init__.py)

#from ..service.tag_service import * #ImportError: attempted relative import beyond top-level package


from service.tag_service import *
from flask_restx import Resource, Namespace, fields

tag_ns = Namespace("tag", description="Tag operations")

tag_DTO = tag_ns.model('Tag', {
    'id': fields.Integer(readOnly=True, description='The tag unique identifier'),
    'name': fields.String(required=True, description='The tag name'),
    'description': fields.String(required=False, description='The tag description')
})

@tag_ns.route("/")
class TagList(Resource):
    @tag_ns.doc('list_tags')
    @tag_ns.marshal_list_with(tag_DTO)
    def get(self):
        """List all tags"""
        #return Tag.query.all()
        return "List all tags"

#att
