from flask_restx import Namespace, fields

from app.main.model import OPERATION_TYPES
from app.main.util.action_dto import ActionDTO

_action = ActionDTO.action_name
from app.main.service import CustomDateTime


class HistoryNursingPrescriptionActionDTO:
    api = Namespace(
        "history_nursing_prescription_action",
        description="history nursing prescription action related operations",
    )

    history_nursing_prescription_action = api.model(
        "history_nursing_prescription_action",
        {
            "action": fields.Nested(_action),
            "operation_type": fields.String(
                description="operation type", enum=OPERATION_TYPES
            ),
            "performed_at": CustomDateTime(
                description="action performed date and time",
            ),
        },
    )
