from models import Tag
from config import db
def get_all_tags():
    return Tag.query.all()

def save_new_tag(data):
    tag = Tag.query.filter_by(name=data["name"]).first()
    if not tag:
        new_tag = Tag(
            name=data.get("name"),
            description=data.get("description"),
        )
        
        db.session.add(new_tag)
        db.session.commit()
        
        response_object = {
            "status": "success",
            "message": "Tag successfully created.",
        }
        return response_object, 201
    else:
        response_object = {
            "status": "fail",
            "message": "Tag already exists.",
        }
        return response_object, 409

def get_tag_by_id(tag_id):
    return Tag.query.filter_by(id=tag_id).first()

def update_tag_by_id(tag_id, data):
    tag = Tag.query.filter_by(id=tag_id).first()
    if tag:
        tag.name = data.get("name")
        tag.description = data("description")
        db.session.commit()
        response_object = {
            "status": "success",
            "message": "Tag successfully updated.",
        }
        return response_object, 200
    else:
        response_object = {
            "status": "fail",
            "message": "Tag does not exist.",
        }
        return response_object, 404

def delete_tag_by_id(tag_id):
    tag = Tag.query.filter_by(id=tag_id).first()
    if tag:
        db.session.delete(tag)
        db.session.commit()
        response_object = {
            "status": "success",
            "message": "Tag successfully deleted.",
        }
        return response_object, 200
    else:
        response_object = {
            "status": "fail",
            "message": "Tag does not exist.",
        }
        return response_object, 404
