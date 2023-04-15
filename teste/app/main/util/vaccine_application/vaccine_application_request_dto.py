from flask_restx import Namespace, fields

from app.main.model import REQUEST_STATUS
from app.main.util.patient_dto import PatientDTO
from app.main.util.professional_dto import ProfessionalDTO
from app.main.util.vaccine.vaccine_dto import VaccineDTO


class VaccineApplicationRequestDTO:

    api = Namespace(
        "vaccine_application_request",
        description="vaccine application request related operations",
    )

    vaccine_application_request_id = {
        "id": fields.Integer(description="vaccine application id", example=1),
    }

    vaccine_application_request_professional_id = {
        "professional_id": fields.Integer(
            required=True, description="professional relationship", example=1
        ),
    }

    vaccine_application_request_patient_id = {
        "patient_id": fields.Integer(
            required=True, description="patient relationship", example=1
        ),
    }

    vaccine_application_request_vaccine_id = {
        "vaccine_id": fields.Integer(
            required=True, description="vaccine relationship", example=1
        ),
    }

    vaccine_application_request_status = {
        "status": fields.String(
            required=True, description="request status", enum=REQUEST_STATUS
        ),
    }

    vaccine_application_request_observations = {
        "observations": fields.Integer(
            description="vaccine application request observations"
        ),
    }

    vaccine_application_request_post = api.model(
        "vaccine_application_request_post",
        vaccine_application_request_professional_id
        | vaccine_application_request_patient_id
        | vaccine_application_request_vaccine_id
        | vaccine_application_request_observations,
    )

    vaccine_application_request_put = api.clone(
        "vaccine_application_request_put", vaccine_application_request_post
    )

    vaccine_application_request_response = api.model(
        "vaccine_application_request_response",
        vaccine_application_request_id
        | {
            "professional": fields.Nested(
                api.model(
                    "vaccine_application_request_response_professional",
                    ProfessionalDTO.professional_name
                    | ProfessionalDTO.professional_social_name,
                ),
                description="professional info",
            ),
            "patient": fields.Nested(
                api.model(
                    "vaccine_application_request_response_patient",
                    PatientDTO.patient_name | PatientDTO.patient_social_name,
                ),
                description="patient info",
            ),
            "vaccine": fields.Nested(
                api.model(
                    "vaccine_application_request_response_vaccine",
                    VaccineDTO.vaccine_name,
                ),
                description="vaccine info",
            ),
        }
        | vaccine_application_request_status,
    )

    vaccine_application_request_list = api.model(
        "vaccine_application_request_list",
        {
            "current_page": fields.Integer(),
            "total_items": fields.Integer(),
            "total_pages": fields.Integer(),
            "items": fields.List(fields.Nested(vaccine_application_request_response)),
        },
    )
