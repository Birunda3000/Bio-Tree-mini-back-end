from app.main import db
from app.main.exceptions import DefaultException
from app.main.model import Queue

QUEUES = [
    "Acolhimento",
    "Atendimento Médico",
    "Sala de Observação",
    "Sala de Internação",
    "Vacinação",
]


def create_default_queues() -> None:
    for queue in QUEUES:
        db.session.add(Queue(name=queue))
    db.session.commit()


def get_queues() -> list[Queue]:
    return Queue.query.all()


def get_queue(queue_id: int, options: list = None) -> Queue:

    query = Queue.query

    if options is not None:
        query = query.options(*options)

    queue = query.get(queue_id)

    if queue is None:
        raise DefaultException("queue_not_found", code=404)

    return queue
