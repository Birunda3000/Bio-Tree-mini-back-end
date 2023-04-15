from datetime import date, timedelta

from app.main import db
from app.main.exceptions import DefaultException
from app.main.model import VaccineApplication


def save_new_vaccine_application_maintenance(data: dict[str, any]) -> None:
    vaccine_application = get_vaccine_application(
        vaccine_application_id=data.get("vaccine_application_id")
    )

    if vaccine_application.application_type != "Aplicação":
        raise DefaultException(
            "vaccine_application_maintenance_not_accepted_application_type", code=409
        )

    if vaccine_application.edited or vaccine_application.deleted:
        raise DefaultException(
            "vaccine_application_maintenance_invalid_vaccine_application",
            code=409,
        )

    if vaccine_application.performed_at < (date.today() - timedelta(days=30)):
        raise DefaultException(
            "vaccine_application_maintenance_vaccine_application_time_exceeded",
            code=409,
        )

    vaccine_application.edited = True

    new_vaccine_application = VaccineApplication(
        application=vaccine_application,
        professional=vaccine_application.professional,
        patient=vaccine_application.patient,
        vaccine_name=vaccine_application.vaccine_name,
        application_type=vaccine_application.application_type,
        batch=vaccine_application.batch,
        manufacturer=vaccine_application.manufacturer,
        administration_route=vaccine_application.administration_route,
        application_site=vaccine_application.application_site,
        pregnancy_type=vaccine_application.pregnancy_type,
        complement=vaccine_application.complement,
        performed_at=date_from_string(
            data.get("performed_at"),
        ),
    )

    db.session.add(new_vaccine_application)
    db.session.commit()


def delete_vaccine_application_maintenance(
    vaccine_application_id: int, data: dict[str, any]
):
    vaccine_application = get_vaccine_application(
        vaccine_application_id=vaccine_application_id
    )

    if vaccine_application.application_type != "Aplicação":
        raise DefaultException(
            "vaccine_application_maintenance_not_accepted_application_type", code=409
        )

    if vaccine_application.edited or vaccine_application.deleted:
        raise DefaultException(
            "vaccine_application_maintenance_invalid_vaccine_application",
            code=409,
        )

    if vaccine_application.performed_at < (date.today() - timedelta(days=30)):
        raise DefaultException(
            "vaccine_application_maintenance_vaccine_application_time_exceeded",
            code=409,
        )

    delete_reason = data.get("delete_reason")

    vaccine_application.deleted = True
    vaccine_application.delete_reason = delete_reason

    db.session.commit()


from app.main.service.custom_fields.custom_date_service import date_from_string
from app.main.service.vaccine_application.vaccine_application_service import (
    get_vaccine_application,
)
