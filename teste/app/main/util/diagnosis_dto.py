from flask_restx import Namespace, fields

from app.main.util.protocol_dto import ProtocolDTO

_protocol = ProtocolDTO.protocol_response


class DiagnosisDTO:
    api = Namespace("diagnosis", description="diagnosis related operations")

    diagnosis_post = api.model(
        "diagnosis_create",
        {
            "protocol_id": fields.Integer(required=True, description="protocol id"),
            "questions_ids": fields.List(
                fields.Integer, required=True, description="questions ids"
            ),
        },
    )

    question = api.model(
        "question",
        {
            "id": fields.Integer(description="room id"),
            "name": fields.String(required=True, description="protocol name"),
        },
    )

    diagnosis_response = api.model(
        "diagnosis_response",
        {
            "protocol": fields.Nested(_protocol),
            "questions": fields.List(
                fields.String, required=True, description="questions list"
            ),
        },
    )

    diagnosis_response_with_id = api.model(
        "diagnosis_response_by_id",
        {
            "id": fields.Integer(description="room id"),
            "protocol": fields.Nested(_protocol),
            "questions": fields.List(fields.Nested(question)),
        },
    )

    diagnoses_list = api.model(
        "diagnoses_list",
        {
            "current_page": fields.Integer(),
            "total_items": fields.Integer(),
            "total_pages": fields.Integer(),
            "items": fields.List(fields.Nested(diagnosis_response_with_id)),
        },
    )
