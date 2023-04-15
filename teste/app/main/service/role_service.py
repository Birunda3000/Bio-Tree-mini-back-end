from sqlalchemy.orm import joinedload

from app.main import db
from app.main.exceptions import DefaultException, ValidationException
from app.main.model import Resource, Role


def get_all_roles(params: dict[str, str]) -> list[Role]:

    name = params.get("name", type=str)

    filters = []

    if name:
        filters.append(Role.name.ilike(f"%{name}%"))

    return Role.query.options(joinedload("resources")).filter(*filters).all()


def save_new_role(data: dict[str, str]) -> None:
    _resources_not_empty_or_400(resources=data.get("resources"))

    if _role_exists_by_name(data.get("name")):
        raise DefaultException("role_in_use", code=409)

    resources = _get_resources_from_database(resources=data.get("resources"))

    new_role = Role(name=data.get("name"), resources=resources)

    db.session.add(new_role)
    db.session.commit()


def update_role(role_id: int, data: dict[str, str]) -> None:
    _resources_not_empty_or_400(resources=data.get("resources"))

    role = get_role(role_id=role_id)

    if role.is_default:
        raise DefaultException("role_is_default", code=409)

    if data.get("name") != role.name and _role_exists_by_name(data.get("name")):
        raise DefaultException("role_in_use", code=409)

    resource_codes = [resource.code for resource in role.resources]

    if set(data.get("resources")) != set(resource_codes):
        new_resources = _get_resources_from_database(data.get("resources"))
        role.resources = new_resources

    role.name = data.get("name")

    db.session.commit()


def delete_role(role_id: int) -> None:
    role = get_role(role_id=role_id)

    if role.is_default:
        raise DefaultException("role_is_default", code=409)

    db.session.delete(role)
    db.session.commit()


def get_role(role_id: int, options: list = None) -> Role:

    query = Role.query

    if options is not None:
        query = query.options(*options)

    role = query.get(role_id)

    if role is None:
        raise DefaultException("role_not_found", code=404)

    return role


def create_default_roles() -> None:
    resources = Resource.query.all()

    db.session.add(Role(name="Administrador", resources=resources, is_default=True))
    db.session.commit()


def _resources_not_empty_or_400(resources: list[str]) -> None:
    if not resources:
        raise ValidationException(
            errors={"resources": "resource_invalid"}, message="resource_invalid"
        )


def _role_exists_by_name(role_name: str) -> bool:
    return (
        Role.query.with_entities(Role.id).filter_by(name=role_name).first() is not None
    )


def _get_resources_from_database(resources: list[str]) -> list[Resource]:
    return Resource.query.filter(Resource.code.in_(resources)).all()
