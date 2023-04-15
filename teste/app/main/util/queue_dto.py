from flask_restx import Namespace, fields


class QueueDTO:
    api = Namespace("queue", description="queue related operations")

    queue = api.model(
        "queue_response",
        {
            "id": fields.Integer(description="queue id"),
            "name": fields.String(description="queue name"),
        },
    )
