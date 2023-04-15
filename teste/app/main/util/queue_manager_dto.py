from flask_restx import Namespace, fields

from app.main.model import PRIORITY_OPTIONS, RISK_CLASSIFICATIONS
from app.main.service import CustomDate


class QueueManagerDTO:
    api = Namespace("queue_manager", description="queue_manager related operations")

    queue_manager_post = api.model(
        "queue_manager_insert_patient",
        {
            "queue_id": fields.Integer(description="queue id", required=True),
            "patient_id": fields.Integer(description="patient id", required=True),
            "priority_type": fields.String(
                description="type of patient priority", enum=PRIORITY_OPTIONS
            ),
        },
    )

    queue_manager_response = api.model(
        "queue_manager_response",
        {
            "id": fields.Integer(description="queue manager ID"),
            "patient_id": fields.Integer(description="patient id"),
            "patient_name": fields.String(description="patient name"),
            "priority": fields.Boolean(
                description="whether the patient has priority in the queue"
            ),
            "priority_type": fields.String(
                description="type of patient priority", enum=PRIORITY_OPTIONS
            ),
            "status": fields.String(description="patient status"),
            "queue_entry": CustomDate(
                description="time the patient entered the queue",
            ),
            "risk_classification": fields.String(
                description="patient risk classification. None if risk classification not done",
                enum=RISK_CLASSIFICATIONS,
            ),
        },
    )

    patientes_by_queue = api.model(
        "patients_by_queue",
        {
            "current_page": fields.Integer(description="pagination current page"),
            "total_items": fields.Integer(description="total number of patients"),
            "total_pages": fields.Integer(description="pagintation total pages"),
            "total_priority": fields.Integer(description="number of priority patients"),
            "items": fields.List(
                fields.Nested(queue_manager_response), description="queue patients"
            ),
        },
    )

    queue_manager_remove_from_queue = api.model(
        "queue_manager_remove_from queue",
        {
            "professional_id": fields.Integer(
                description="professional id", required=False
            ),
        },
    )

    queue_manager_change_patient_queue = api.model(
        "queue_manager_change_patient_queue",
        {
            "patient_id": fields.Integer(description="patient id", required=True),
            "queue_id": fields.Integer(description="queue id", required=True),
            "professional_id": fields.Integer(
                description="identifier of the professional who handled the patient",
                required=False,
            ),
        },
    )
