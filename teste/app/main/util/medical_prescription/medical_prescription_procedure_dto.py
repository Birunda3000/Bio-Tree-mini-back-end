from flask_restx import Namespace, fields

from app.main.util.procedure_dto import ProcedureDTO

_procedure_description = ProcedureDTO.procedure_description
from app.main.service import CustomDateTime


class MedicalPrescriptionProcedureDTO:

    api = Namespace(
        "medical_prescription_procedure",
        description="medical prescription procedure related operations",
    )

    medical_prescription_procedure_description = api.model(
        "medical_prescription_procedure_description",
        {
            "procedure": fields.Nested(_procedure_description),
        },
    )

    medical_prescription_procedure_response = api.model(
        "medical_prescription_procedure_response",
        {
            "procedure": fields.Nested(_procedure_description),
            "execute_at": CustomDateTime(
                description="medicine execution date and time",
            ),
            "observations": fields.String(
                description="procedure observation", example="Procedure Observation"
            ),
        },
    )

    medical_prescription_procedure_post = api.model(
        "medical_prescription_procedure_post",
        {
            "procedure_id": fields.Integer(
                required=True, description="procedure relationship", example=1
            ),
            "execute_at": CustomDateTime(
                required=True,
                description="medicine execution date and time",
            ),
            "observations": fields.String(
                description="procedure observation", example="Procedure Observation"
            ),
        },
    )
