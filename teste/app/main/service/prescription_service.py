from math import ceil

from sqlalchemy.orm import joinedload
from werkzeug.datastructures import ImmutableMultiDict

from app.main import db
from app.main.config import Config
from app.main.exceptions import DefaultException
from app.main.model import Action, Prescription, Protocol

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def get_prescriptions(params: ImmutableMultiDict):

    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)
    protocol = params.get("protocol", type=str)

    filters = []

    if protocol:
        filters.append(Protocol.name.ilike(f"%{protocol}%"))

    pagination = (
        Prescription.query.options(joinedload("actions"), joinedload("protocol"))
        .join(Protocol)
        .filter(*filters)
        .order_by(Prescription.id)
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return {
        "current_page": page,
        "total_items": pagination.total,
        "total_pages": ceil(pagination.total / per_page),
        "items": pagination.items,
    }


def get_prescription_by_id(prescription_id: int) -> Prescription:
    return get_prescription(
        prescription_id=prescription_id,
        options=[joinedload("actions"), joinedload("protocol")],
    )


def save_new_prescription(data: dict[str, str]) -> None:
    protocol = _get_protocol_and_validate(protocol_id=data.get("protocol_id"))

    actions_ids = set(data.get("actions_ids"))

    actions = _get_actions_and_validate(actions_ids=actions_ids)

    new_prescription = Prescription(protocol=protocol, actions=actions)

    db.session.add(new_prescription)
    db.session.commit()


def update_prescription(prescription_id: int, data: dict[str, str]) -> None:
    prescription = get_prescription(
        prescription_id=prescription_id, options=[joinedload("actions")]
    )

    if change_protocol := prescription.protocol_id != data.get("protocol_id"):
        new_protocol = _get_protocol_and_validate(protocol_id=data.get("protocol_id"))

    new_actions_ids = set(data.get("actions_ids"))

    prescription_actions_ids = set(action.id for action in prescription.actions)

    if prescription_actions_ids != new_actions_ids:
        new_actions = _get_actions_and_validate(actions_ids=new_actions_ids)
        prescription.actions = new_actions

    if change_protocol:
        prescription.protocol = new_protocol

    db.session.commit()


def delete_prescription(prescription_id: int) -> None:
    prescription = get_prescription(prescription_id=prescription_id)

    db.session.delete(prescription)
    db.session.commit()


def get_prescription(prescription_id: int, options: list = None) -> Prescription:

    query = Prescription.query

    if options is not None:
        query = query.options(*options)

    prescription = query.get(prescription_id)

    if prescription is None:
        raise DefaultException("prescription_not_found", code=404)

    return prescription


def _get_protocol_and_validate(protocol_id: int) -> Protocol:
    protocol = get_protocol(
        protocol_id=protocol_id, options=[joinedload("prescription")]
    )

    if protocol.protocol_type != "Prescrição":
        raise DefaultException("protocol_is_not_prescription_type", code=409)

    if protocol.prescription:
        raise DefaultException(
            "protocol_already_associated_with_prescription", code=409
        )

    return protocol


def _get_actions_and_validate(actions_ids: set[int]) -> list[Action]:
    actions = Action.query.filter(Action.id.in_(actions_ids)).all()

    actions_ids_db = set(action.id for action in actions)

    if actions_ids != actions_ids_db:
        raise DefaultException("action_not_found", code=404)

    return actions


from app.main.service.protocol_service import get_protocol
