import datetime
from math import ceil

from sqlalchemy import func
from werkzeug.datastructures import ImmutableMultiDict

from app.main import db
from app.main.config import Config
from app.main.exceptions import DefaultException
from app.main.model import Patient, Queue, QueueLog, QueueManager, RiskClassification

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def add_patient_in_queue(data: dict[str, any]) -> None:

    queue_id = data.get("queue_id")
    patient_id = data.get("patient_id")
    priority_type = data.get("priority_type")

    queue_name = _get_queue_name_or_404(queue_id=queue_id)

    get_patient(patient_id=patient_id)

    queue_manager = get_queue_manager_by_patient_id(patient_id=patient_id)

    # Patient is entering hospital
    if not queue_manager:
        queue_manager = QueueManager(
            patient_id=patient_id,
            queue_id=queue_id,
            priority=priority_type is not None,
            priority_type=priority_type,
            status=f"Aguardando {queue_name}",
        )
    elif queue_manager.queue_id is not None:
        raise DefaultException("patient_already_in_queue", code=409)
    # Patient is in hospital but not in queue
    else:
        queue_manager.last_queue_entry = datetime.datetime.now()
        queue_manager.queue_id = queue_id
        queue_manager.status = f"Aguardando {queue_name}"

    db.session.add(queue_manager)

    queue_log = QueueLog(queue_id=queue_id, queue_manager=queue_manager)

    db.session.add(queue_log)
    db.session.commit()


def is_patient_in_queue(patient_id: int, queue_id: int) -> bool:

    get_patient(patient_id=patient_id)

    queue_manager = get_queue_manager_by_patient_id(patient_id=patient_id)

    if not queue_manager:
        return False
    if not queue_manager.queue_id:
        return False
    if queue_manager.queue_id != queue_id:
        return False

    return True


def get_patients_queue(queue_id: int, params: ImmutableMultiDict) -> list[QueueManager]:

    _queue_exists_or_404(queue_id=queue_id)

    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)

    filters = [QueueManager.queue_id == queue_id, QueueManager.hospital_exit.is_(None)]

    pagination = (
        QueueManager.query.with_entities(
            QueueManager.id,
            QueueManager.patient_id,
            Patient.name.label("patient_name"),
            QueueManager.priority,
            QueueManager.priority_type,
            QueueManager.status,
            QueueManager.last_queue_entry.label("queue_entry"),
            RiskClassification.risk_classification,
        )
        .select_from(QueueManager)
        .join(Patient)
        .join(RiskClassification, isouter=True)
        .filter(*filters)
        .order_by(
            db.case(
                (RiskClassification.risk_classification == "Emergência", 1),
                (RiskClassification.risk_classification == "Muito Urgente", 2),
                (RiskClassification.risk_classification == "Urgente", 3),
                (RiskClassification.risk_classification == "Pouco Urgente", 4),
                (RiskClassification.risk_classification == "Não Urgente", 5),
                else_=6,
            ),
            QueueManager.priority.is_(True).desc(),
            QueueManager.last_queue_entry,
        )
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    total_priority = (
        QueueManager.query.with_entities(func.count(QueueManager.priority))
        .join(QueueLog)
        .filter(
            QueueLog.queue_id == queue_id,
            QueueLog.queue_exit.is_(None),
            QueueManager.priority.is_(True),
        )
        .scalar()
    )

    return {
        "current_page": page,
        "total_items": pagination.total,
        "total_pages": ceil(pagination.total / per_page),
        "total_priority": total_priority,
        "items": pagination.items,
    }


def remove_patient_from_queue(patient_id: int, data: dict[str, str] = {}) -> None:

    removed_from_queue = get_queue_manager_by_patient_id(patient_id=patient_id)

    if not removed_from_queue:
        raise DefaultException("patient_not_entered_hospital", code=404)

    if removed_from_queue.queue_id is None:
        raise DefaultException("patient_not_in_queue", code=409)

    queue_log = QueueLog.query.filter(
        QueueLog.queue_manager == removed_from_queue, QueueLog.queue_exit.is_(None)
    ).first()

    if "professional_id" in data:
        professional_id = data.get("professional_id")
        get_professional(professional_id=professional_id)
        queue_log.professional_id = professional_id

    queue_log.queue_exit = datetime.datetime.now()

    removed_from_queue.queue_id = None
    removed_from_queue.status = "Em espera"

    db.session.add(queue_log)
    db.session.add(removed_from_queue)
    db.session.commit()


def close_queue_manager(patient_id: int) -> None:

    queue_manager = get_queue_manager_by_patient_id(patient_id=patient_id)

    if not queue_manager:
        raise DefaultException("patient_not_entered_hospital", code=404)
    elif queue_manager.queue_id is not None:
        raise DefaultException("patient_in_queue", code=409)

    queue_manager.status = "De alta"
    queue_manager.hospital_exit = datetime.datetime.now()

    db.session.add(queue_manager)
    db.session.commit()


def change_patient_queue(data: dict) -> None:
    queue_id = data.get("queue_id")
    patient_id = data.get("patient_id")

    queue_name = _get_queue_name_or_404(queue_id=queue_id)

    get_patient(patient_id=patient_id)

    queue_manager = get_queue_manager_by_patient_id(patient_id=patient_id)

    if not queue_manager:
        raise DefaultException("patient_not_entered_hospital", code=404)
    elif queue_manager.queue_id is None:
        raise DefaultException("patient_not_in_queue", code=409)
    elif queue_manager.queue_id == queue_id:
        raise DefaultException("patient_already_in_destination_queue", code=409)

    queue_log = QueueLog.query.filter(
        QueueLog.queue_manager == queue_manager, QueueLog.queue_exit.is_(None)
    ).first()

    if "professional_id" in data:
        professional_id = data.get("professional_id")
        get_professional(professional_id=professional_id)
        queue_log.professional_id = professional_id

    queue_log.queue_exit = datetime.datetime.now()
    db.session.add(queue_log)

    queue_manager.last_queue_entry = datetime.datetime.now()
    queue_manager.queue_id = queue_id
    queue_manager.status = f"Aguardando {queue_name}"

    db.session.add(queue_manager)

    new_queue_log = QueueLog(queue_id=queue_id, queue_manager=queue_manager)

    db.session.add(new_queue_log)
    db.session.commit()


def _get_queue_name_or_404(queue_id: int) -> str:
    queue_name = (
        Queue.query.with_entities(Queue.name).filter(Queue.id == queue_id).scalar()
    )

    if not queue_name:
        raise DefaultException("queue_not_found", code=404)

    return queue_name


def _queue_exists_or_404(queue_id: int) -> None:
    queue_exists = (
        Queue.query.with_entities(Queue.id).filter(Queue.id == queue_id).scalar()
        is not None
    )

    if not queue_exists:
        raise DefaultException("queue_not_found", code=404)


def get_queue_manager_by_patient_id(patient_id: int) -> QueueManager:
    return QueueManager.query.filter(
        QueueManager.patient_id == patient_id, QueueManager.hospital_exit.is_(None)
    ).first()


def get_queue_manager(queue_manager_id: int, options: list = None) -> QueueManager:

    query = QueueManager.query

    if options is not None:
        query = query.options(*options)

    queue_manager = query.get(queue_manager_id)

    if queue_manager is None:
        raise DefaultException("queue_manager_not_found", code=404)

    return queue_manager


from app.main.service.patient_service import get_patient
from app.main.service.professional_service import get_professional
