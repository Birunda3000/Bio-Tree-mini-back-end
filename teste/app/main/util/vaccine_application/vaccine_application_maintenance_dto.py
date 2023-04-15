from flask_restx import Namespace, fields

from app.main.service import CustomDatePast


class VaccineApplicationMaintenanceDTO:

    api = Namespace(
        "vaccine_application_maintenance",
        description="vaccine application maintenance related operations",
    )

    vaccine_application_maintenance_application_id = {
        "vaccine_application_id": fields.Integer(
            required=True, description="vaccine application relationship", example=1
        )
    }

    vaccine_application_maintenance_performed_at = {
        "performed_at": CustomDatePast(
            required=True,
            description="vaccine application execution date",
        )
    }

    vaccine_application_maintenance_reason = {
        "reason": fields.String(
            required=True,
            description="vaccine application reason for exclusion",
        )
    }

    vaccine_application_maintenance_post = api.model(
        "vaccine_application_maintenance_post",
        vaccine_application_maintenance_application_id
        | vaccine_application_maintenance_performed_at,
    )

    vaccine_application_maintenance_delete = api.model(
        "vaccine_application_maintenance_delete",
        vaccine_application_maintenance_reason,
    )
