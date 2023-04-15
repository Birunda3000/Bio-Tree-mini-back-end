from flask_restx import Namespace, fields

from app.main.service import CustomDateTime
from app.main.util.vital_signs_control_dto import VitalSignsControlDTO

_vital_signs_control = VitalSignsControlDTO.vital_signs_control


class SaeDTO:

    api = Namespace(
        "systematization_of_nursing_care",
        description="systematization of nursing care (SAE) related operations",
    )

    action_sae = api.model(
        "action_sae",
        {
            "id": fields.Integer(description="action id", required=True, example=1),
            "recurrence": fields.String(
                description="action recurrence", max_length=50, required=True
            ),
        },
    )

    sae_determinations_post = api.model(
        "sae_prescriptions_diagnosis",
        {
            "admission_id": fields.Integer(
                description="admission relationship", required=True, example=1
            ),
            "professional_id": fields.Integer(
                description="professional relationship", required=True, example=1
            ),
            "actions": fields.List(fields.Nested(action_sae), required=True),
            "questions": fields.List(
                fields.Integer(description="question id"), required=True
            ),
        },
    )

    prescription_performed = api.model(
        "prescription_performed",
        {
            "action_id": fields.Integer(
                description="action relationship", required=True, example=1
            ),
            "performed_at": CustomDateTime(description="time performed", required=True),
            "delete": fields.Boolean(
                description="delete action", default=False, required=True
            ),
        },
    )

    sae_post = api.model(
        "sae_post",
        {
            "admission_id": fields.Integer(
                description="admission relationship", required=True, example=1
            ),
            "professional_id": fields.Integer(
                description="professional relationship", required=True, example=1
            ),
            "vital_signs_control": fields.Nested(_vital_signs_control),
            "prescriptions_performed": fields.List(
                fields.Nested(prescription_performed)
            ),
        },
    )

    sae_get = api.model(
        "sae_get",
        {
            "admission_id": fields.Integer(
                description="sae relationship", required=True, example=1
            )
        },
    )

    sae_actions_get = api.clone(
        "sae_actions_get",
        action_sae,
        {"name": fields.String(description="action name")},
    )

    sae_questions_get = api.model(
        "sae_questions_get",
        {
            "id": fields.Integer(description="question id"),
            "name": fields.String(description="question name"),
        },
    )

    sae_response = api.model(
        "sae_response",
        {
            "questions": fields.List(fields.Nested(sae_questions_get)),
            "actions": fields.List(fields.Nested(sae_actions_get)),
        },
    )

    questions_sae_delete = api.model(
        "questions_sae_delete",
        {
            "admission_id": fields.Integer(
                description="admission relationship", required=True, example=1
            ),
            "professional_id": fields.Integer(
                description="professional id", required=True, example=1
            ),
            "questions": fields.List(
                fields.Integer(description="question id"), required=True
            ),
        },
    )
