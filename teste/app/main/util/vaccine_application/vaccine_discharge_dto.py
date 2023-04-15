from flask_restx import Namespace, fields

from app.main.model import (
    ADMINISTRATION_ROUTES,
    APPLICATION_SITES,
    APPLICATION_TYPES,
    COMPLEMENT_TYPES,
    PREGNANCY_TYPES,
)
from app.main.service import CustomDatePast


class VaccineDischargeDTO:

    api = Namespace(
        "vaccine_discharge", description="vaccine discharge related operations"
    )

    vaccine_discharge_post = api.model(
        "vaccine_discharge_create",
        {
            "professional_id": fields.Integer(
                required=True, description="professional relationship", example=1
            ),
            "patient_id": fields.Integer(
                required=True, description="patient relationship", example=1
            ),
            "vaccine_name": fields.String(
                required=True,
                description="vaccine name",
            ),
            "manufacturer": fields.String(
                description="vaccine discharge manufacturer",
            ),
            "batch": fields.String(
                description="vaccine discharge batch",
            ),
            "administration_route": fields.String(
                enum=ADMINISTRATION_ROUTES,
                description="vaccine discharge administration route",
            ),
            "application_site": fields.String(
                enum=APPLICATION_SITES,
                description="vaccine discharge site",
            ),
            "pregnancy_type": fields.String(
                required=True,
                enum=PREGNANCY_TYPES,
                description="vaccine discharge pregnancy type",
            ),
            "complement": fields.String(
                required=True,
                enum=COMPLEMENT_TYPES,
                description="vaccine discharge complement",
            ),
            "performed_at": CustomDatePast(
                description="vaccine discharge execution date",
            ),
        },
    )
