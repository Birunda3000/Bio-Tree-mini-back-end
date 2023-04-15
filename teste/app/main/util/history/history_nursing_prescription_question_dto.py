from flask_restx import Namespace, fields

from app.main.model import OPERATION_TYPES
from app.main.util.question_dto import QuestionDTO

_question = QuestionDTO.question_name


class HistoryNursingPrescriptionQuestionDTO:
    api = Namespace(
        "history_nursing_prescription_question",
        description="history nursing prescription question related operations",
    )

    history_nursing_prescription_question = api.model(
        "history_nursing_prescription_question",
        {
            "operation_type": fields.String(
                description="operation type", enum=OPERATION_TYPES
            ),
            "question": fields.Nested(_question),
        },
    )
