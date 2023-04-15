from math import ceil

from sqlalchemy.orm import joinedload
from werkzeug.datastructures import ImmutableMultiDict

from app.main import db
from app.main.config import Config
from app.main.exceptions import DefaultException, ValidationException
from app.main.model import PROTOCOL_TYPES, Protocol

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def get_protocols(params: ImmutableMultiDict):

    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)
    name = params.get("name", type=str)
    protocol_type = params.get("protocol_type", type=str)

    filters = []

    if name:
        filters.append(Protocol.name.ilike(f"%{name}"))

    if protocol_type:
        if protocol_type in PROTOCOL_TYPES:
            filters.append(Protocol.protocol_type == protocol_type)
        else:
            raise ValidationException(
                errors={"protocol_type": "Protocol is not in ENUM"},
                message="invalid_protocol_type",
            )

    pagination = (
        Protocol.query.filter(*filters)
        .order_by(Protocol.id)
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return {
        "current_page": page,
        "total_items": pagination.total,
        "total_pages": ceil(pagination.total / per_page),
        "items": pagination.items,
    }


def get_protocol_by_id(protocol_id: int):
    return get_protocol(protocol_id=protocol_id)


def save_new_protocol(data: dict[str, any]):

    protocol = Protocol.query.filter(
        (Protocol.name == data.get("name").upper()),
        (Protocol.protocol_type == data.get("protocol_type")),
    ).first()

    if protocol:
        raise DefaultException("name_in_use", code=409)

    new_protocol = Protocol(
        name=data.get("name"), protocol_type=data.get("protocol_type")
    )

    db.session.add(new_protocol)
    db.session.commit()


def update_protocol(protocol_id: int, data: dict[str, any]) -> None:

    protocol_type = data.get("protocol_type")

    protocol = get_protocol(
        protocol_id=protocol_id,
        options=[joinedload("diagnosis"), joinedload("prescription")],
    )

    if protocol.protocol_type != protocol_type:
        if protocol.protocol_type == "Diagnóstico" and protocol.diagnosis:
            raise DefaultException("protocol_is_associated_with_diagnosis", code=409)
        elif protocol.prescription:
            raise DefaultException("protocol_is_associated_with_prescription", code=409)

    filters = [
        (Protocol.name == data.get("name").upper()),
        (Protocol.protocol_type == data.get("protocol_type")),
    ]

    change_protocol = Protocol.query.filter(*filters).first()

    if change_protocol is not None:
        raise DefaultException("protocol_already_exist", code=409)

    protocol.name = data.get("name")
    protocol.protocol_type = data.get("protocol_type")

    db.session.commit()


def delete_protocol(protocol_id: int) -> None:
    protocol = get_protocol(protocol_id=protocol_id)

    if protocol.protocol_type == "Diagnóstico" and protocol.diagnosis:
        raise DefaultException("protocol_is_associated_with_diagnosis", code=409)

    elif protocol.prescription:
        raise DefaultException("protocol_is_associated_with_prescription", code=409)

    db.session.delete(protocol)
    db.session.commit()


def get_protocol(protocol_id: int, options: list = None) -> Protocol:

    query = Protocol.query

    if options is not None:
        query = query.options(*options)

    protocol = query.get(protocol_id)

    if protocol is None:
        raise DefaultException("protocol_not_found", code=404)

    return protocol
