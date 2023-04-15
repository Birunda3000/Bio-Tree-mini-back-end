import re

from app.main import db
from app.main.exceptions import DefaultException
from app.main.model import Resource

RESOURCES_NAME = ["Atendimento", "Gerenciamento de paciente"]


def get_all_resources() -> list[Resource]:
    return Resource.query.all()


def create_default_resources() -> None:
    for resource in RESOURCES_NAME:
        db.session.add(Resource(name=resource, code=create_code(resource)))
    db.session.commit()


def create_code(name: str) -> str:
    # Return name with alphanumeric characters in lowercase
    return re.sub("[^A-Za-z0-9]+", "", name).lower()


def get_resource(resource_id: int, options: list = None) -> Resource:

    query = Resource.query

    if options is not None:
        query = query.options(*options)

    resource = query.get(resource_id)

    if resource is None:
        raise DefaultException("resource_not_found", code=404)

    return resource
