from datetime import date
from math import ceil

from sqlalchemy import case, func
from sqlalchemy.orm import joinedload
from werkzeug.datastructures import ImmutableMultiDict

from app.main import db
from app.main.config import Config
from app.main.exceptions import DefaultException
from app.main.model import DeathLaunch, Patient, Professional

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def get_death_launches(params: ImmutableMultiDict) -> dict[str, any]:
    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)

    patient_name = params.get("patient_name", type=str)
    responsible_for_registration = params.get("responsible_for_registration", type=str)
    start_date_of_death = params.get("start_date_of_death", type=str)
    end_date_of_death = params.get("end_date_of_death", type=str)
    start_registration_date = params.get("start_registration_date", type=str)
    end_registration_date = params.get("end_registration_date", type=str)

    filters = []

    if patient_name:
        filters.append(
            DeathLaunch.patient.has(patient_name_filter(patient_name=patient_name))
        )

    if responsible_for_registration:
        filters.append(
            DeathLaunch.professional.has(
                professional_name_filter(professional_name=responsible_for_registration)
            )
        )

    if start_date_of_death:
        if not end_date_of_death:
            end_date_of_death = date_to_string(date.today())

        filters.append(
            func.date(DeathLaunch.datetime_of_death).between(
                date_from_string(start_date_of_death),
                date_from_string(end_date_of_death),
            )
        )

    if start_registration_date:
        if not end_registration_date:
            end_registration_date = date_to_string(date.today())

        filters.append(
            func.date(DeathLaunch.registration_datetime).between(
                date_from_string(start_registration_date),
                date_from_string(end_registration_date),
            )
        )

    pagination = (
        DeathLaunch.query.with_entities(
            DeathLaunch.id,
            DeathLaunch.datetime_of_death,
            DeathLaunch.registration_datetime,
            Professional.name.label("responsible_for_registration"),
            case(
                (Patient.social_name is not None, Patient.social_name),
                else_=Patient.name,
            ).label("name"),
        )
        .select_from(DeathLaunch)
        .join(Patient)
        .join(Professional)
        .filter(*filters)
        .order_by(DeathLaunch.id)
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return {
        "current_page": page,
        "total_items": pagination.total,
        "total_pages": ceil(pagination.total / per_page),
        "items": pagination.items,
    }


def get_death_launch_by_id(death_launch_id: int) -> DeathLaunch:
    death_launch = DeathLaunch.query.options(
        joinedload("cid_10"),
        joinedload("patient").load_only("id", "name", "social_name", "birth", "sex"),
        joinedload("professional").load_only("id", "name", "social_name"),
    ).get(death_launch_id)

    if not death_launch:
        raise DefaultException("death_launch_not_found", code=404)

    return death_launch


def save_new_death_launch(data: dict[str, any]):
    patient_id = data.get("patient_id")
    professional_id = data.get("professional_id")
    cid_10_id = data.get("cid_10_id")

    patient = get_patient(patient_id=patient_id, options=[joinedload("death_launch")])

    if patient.death_launch:
        raise DefaultException("patient_already_has_death_launch", code=409)

    professional = get_professional(professional_id=professional_id)

    cid_10 = get_cid_10(cid_10_id=cid_10_id)

    new_death_launch = DeathLaunch(
        patient=patient,
        professional=professional,
        cid_10=cid_10,
        certificate_number=data.get("certificate_number"),
        circunstances_of_death=data.get("circunstances_of_death"),
        place=data.get("place"),
        datetime_of_death=datetime_from_string(data.get("datetime_of_death")),
        registration_datetime=datetime_from_string(data.get("registration_datetime")),
    )
    db.session.add(new_death_launch)

    if queue_manager := get_queue_manager_by_patient_id(patient_id=patient_id):
        if queue_manager.queue_id:
            remove_patient_from_queue(
                patient_id=patient_id, data={"patient_id": patient_id}
            )

        close_queue_manager(patient_id=patient_id)
    else:
        db.session.commit()


def update_death_launch(death_launch_id: int, data: dict[str, any]) -> None:
    cid_10_id = data.get("cid_10_id")
    professional_id = data.get("professional_id")

    death_launch = get_death_launch(death_launch_id=death_launch_id)

    if cid_10_id != death_launch.cid_10_id:
        get_cid_10(cid_10_id=cid_10_id)

    if professional_id != death_launch.professional_id:
        get_professional(professional_id=professional_id)

    death_launch.cid_10_id = cid_10_id
    death_launch.professional_id = professional_id
    death_launch.certificate_number = data.get("certificate_number")
    death_launch.circunstances_of_death = data.get("circunstances_of_death")
    death_launch.place = data.get("place")
    death_launch.datetime_of_death = datetime_from_string(data.get("datetime_of_death"))
    death_launch.registration_datetime = datetime_from_string(
        data.get("registration_datetime")
    )

    db.session.commit()


def delete_death_launch(death_launch_id: int) -> None:
    death_launch = get_death_launch(death_launch_id=death_launch_id)

    db.session.delete(death_launch)
    db.session.commit()


def get_death_launch(death_launch_id: int, options: list = None) -> DeathLaunch:

    query = DeathLaunch.query

    if options is not None:
        query = query.options(*options)

    death_launch = query.get(death_launch_id)

    if death_launch is None:
        raise DefaultException("death_launch_not_found", code=404)

    return death_launch


from app.main.service.cid_10_service import get_cid_10
from app.main.service.custom_fields import (
    date_from_string,
    date_to_string,
    datetime_from_string,
)
from app.main.service.filters_service import (
    patient_name_filter,
    professional_name_filter,
)
from app.main.service.patient_service import get_patient
from app.main.service.professional_service import get_professional
from app.main.service.queue_manager_service import (
    close_queue_manager,
    get_queue_manager_by_patient_id,
    remove_patient_from_queue,
)
