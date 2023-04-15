from flask_restx import Namespace, fields

from app.main.model import OPERATION_TYPES
from app.main.service import CustomDateTime


class ClinicalEvolutionDTO:

    api = Namespace(
        "clinical_evolution", description="clinical evolution related operations"
    )

    clinical_evolution_medicine = api.model(
        "clinical_evolution_medicine",
        {
            "id": fields.Integer(
                required=True,
                description="medical prescription medicine relationship",
                example=1,
            ),
            "operation_type": fields.String(
                required=True, description="operation type", enum=OPERATION_TYPES
            ),
            "performed_at": CustomDateTime(
                required=True,
                description="medical prescription medicine performed date and time",
            ),
        },
    )

    clinical_evolution_orientation = api.model(
        "clinical_evolution_orientation",
        {
            "id": fields.Integer(
                required=True,
                description="medical prescription orientation relationship",
                example=1,
            ),
            "operation_type": fields.String(
                required=True, description="operation type", enum=OPERATION_TYPES
            ),
            "performed_at": CustomDateTime(
                required=True,
                description="medical prescription orientation performed date and time",
            ),
        },
    )

    clinical_evolution_procedure = api.model(
        "clinical_evolution_procedure",
        {
            "id": fields.Integer(
                required=True,
                description="medical prescription procedure relationship",
                example=1,
            ),
            "operation_type": fields.String(
                required=True, description="operation type", enum=OPERATION_TYPES
            ),
            "performed_at": CustomDateTime(
                required=True,
                description="medical prescription procedure performed date and time",
            ),
        },
    )

    clinical_evolution_post = api.model(
        "clinical_evolution_post",
        {
            "admission_id": fields.Integer(
                required=True, description="admission relationship", example=1
            ),
            "professional_id": fields.Integer(
                required=True, description="professional relationship", example=1
            ),
            "medical_prescription_medicines_data": fields.List(
                fields.Nested(clinical_evolution_medicine)
            ),
            "medical_prescription_orientations_data": fields.List(
                fields.Nested(clinical_evolution_orientation)
            ),
            "medical_prescription_procedures_data": fields.List(
                fields.Nested(clinical_evolution_procedure)
            ),
        },
    )
