from flask_restx import Namespace, fields

from app.main.model import (
    ADMINISTRATION_ROUTES,
    APPLICATION_SITES,
    APPLICATION_TYPES,
    BOTTLE_TYPES,
    PREGNANCY_TYPES,
)
from app.main.service import CustomDatePast
from app.main.util.patient_dto import PatientDTO


class VaccineApplicationDTO:

    api = Namespace(
        "vaccine_application", description="vaccine application related operations"
    )

    vaccine_application_post = api.model(
        "vaccine_application_create",
        {
            "professional_id": fields.Integer(
                required=True, description="professional relationship", example=1
            ),
            "patient_id": fields.Integer(
                required=True, description="patient relationship", example=1
            ),
            "request_id": fields.Integer(
                required=True,
                description="vaccine application request relationship",
                example=1,
            ),
            "vaccine_name": fields.String(
                required=True,
                description="vaccine name",
            ),
            "manufacturer": fields.String(
                required=True,
                description="vaccine manufacturer",
            ),
            "batch": fields.String(
                required=True,
                description="vaccine batch",
            ),
            "administration_route": fields.String(
                required=True,
                enum=ADMINISTRATION_ROUTES,
                description="vaccine administration route",
            ),
            "application_site": fields.String(
                required=True,
                enum=APPLICATION_SITES,
                description="vaccine application site",
            ),
            "bottle_type": fields.String(
                required=True,
                enum=BOTTLE_TYPES,
                description="bottle type",
            ),
            "bottle_doses_number": fields.Integer(
                required=True, description="bottle doses number", min=1, example=1
            ),
            "pregnancy_type": fields.String(
                required=True,
                enum=PREGNANCY_TYPES,
                description="vaccine application pregnancy type",
            ),
            "performed_at": CustomDatePast(
                required=True,
                description="application execution date and time",
            ),
        },
    )

    vaccine_application_put = api.clone(
        "vaccine_application_put", vaccine_application_post
    )

    vaccine_application_response = api.model(
        "vaccine_application_response",
        {
            "id": fields.Integer(description="vaccine application id"),
            "professional_id": fields.Integer(
                description="professional relationship", example=1
            ),
            "patient": fields.Nested(
                api.model(
                    "vaccine_application_request_response_patient",
                    PatientDTO.patient_id
                    | PatientDTO.patient_name
                    | PatientDTO.patient_social_name
                    | PatientDTO.patient_mother_name,
                ),
                description="patient info",
            ),
            "vaccine_name": fields.String(
                description="vaccine name",
            ),
            "application_type": fields.String(
                enum=APPLICATION_TYPES,
                description="vaccine application type",
            ),
            "manufacturer": fields.String(
                description="vaccine manufacturer",
            ),
            "batch": fields.String(
                description="vaccine batch",
            ),
            "administration_route": fields.String(
                enum=ADMINISTRATION_ROUTES,
                description="vaccine administration route",
            ),
            "application_site": fields.String(
                enum=APPLICATION_SITES,
                description="vaccine application site",
            ),
            "bottle_type": fields.String(
                enum=BOTTLE_TYPES,
                description="bottle type",
            ),
            "bottle_doses_number": fields.Integer(description="bottle doses number"),
            "pregnancy_type": fields.String(
                enum=PREGNANCY_TYPES,
                description="vaccine application pregnancy type",
            ),
            "performed_at": CustomDatePast(
                description="application execution date",
            ),
            "deleted": fields.Boolean(
                description="application delete status",
            ),
            "delete_reason": fields.String(
                description="application delete reason",
            ),
        },
    )

    vaccine_application_list = api.model(
        "vaccine_application_list",
        {
            "current_page": fields.Integer(),
            "total_items": fields.Integer(),
            "total_pages": fields.Integer(),
            "items": fields.List(fields.Nested(vaccine_application_response)),
        },
    )
