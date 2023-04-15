from math import ceil

from sqlalchemy.orm import joinedload
from werkzeug.datastructures import ImmutableMultiDict

from app.main import db
from app.main.config import Config
from app.main.exceptions import DefaultException, ValidationException
from app.main.model import Patient, Professional, QueueManager, RiskClassification

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def get_risk_classification_history(params: ImmutableMultiDict, patient_id: int):

    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)

    patient = get_patient(patient_id=patient_id)

    filters = [RiskClassification.patient_id == patient.id]

    pagination = (
        RiskClassification.query.filter(*filters)
        .order_by(RiskClassification.id)
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return {
        "current_page": page,
        "total_items": pagination.total,
        "total_pages": ceil(pagination.total / per_page),
        "items": pagination.items,
    }


def get_risk_classification(risk_classification_id: int) -> RiskClassification:
    return get_risk_classification(risk_classification_id=risk_classification_id)


def save_risk_classification(data: dict[str, str]) -> None:

    patient_id = data.get("patient_id")
    professional_id = data.get("professional_id")

    patient = get_patient(patient_id=patient_id)

    queue_manager = (
        QueueManager.query.options(joinedload("risk_classification"))
        .filter(
            QueueManager.patient == patient,
            QueueManager.hospital_exit.is_(None),
        )
        .first()
    )

    if queue_manager.risk_classification is not None:
        raise DefaultException("patient_risk_classification_already_exists", code=409)

    professional = get_professional(professional_id=professional_id)

    if data.get("risk_classification") == "Emergência":
        new_risk_classification = RiskClassification(
            patient=patient,
            professional=professional,
            weight=None,
            height=None,
            sys_blood_pressure=None,
            dia_blood_pressure=None,
            temperature=None,
            heart_pulse=None,
            respiratory_frequence=None,
            capillary_blood_glucose=None,
            risk_classification="Emergência",
            queue_manager_id=queue_manager.id,
        )
    else:
        attributes = [
            "weight",
            "sys_blood_pressure",
            "dia_blood_pressure",
            "temperature",
            "heart_pulse",
            "risk_classification",
        ]
        for attribute in attributes:
            if not data.get(attribute):
                raise ValidationException(
                    message="Input payload validation failed",
                    errors={f"{attribute}": f"register_without_{attribute}"},
                )

        new_risk_classification = RiskClassification(
            patient=patient,
            professional=professional,
            weight=data.get("weight"),
            height=data.get("height") or None,
            sys_blood_pressure=data.get("sys_blood_pressure"),
            dia_blood_pressure=data.get("dia_blood_pressure"),
            temperature=data.get("temperature"),
            heart_pulse=data.get("heart_pulse"),
            respiratory_frequence=data.get("respiratory_frequence") or None,
            diabetic=data.get("diabetic"),
            capillary_blood_glucose=data.get("capillary_blood_glucose") or None,
            eye_opening=data.get("eye_opening") or None,
            verbal_response=data.get("verbal_response") or None,
            motor_response=data.get("motor_response") or None,
            pupillary_reactivity=data.get("pupillary_reactivity") or None,
            fasting=data.get("fasting"),
            professional_avaliation=data.get("professional_avaliation"),
            risk_classification=data.get("risk_classification"),
            queue_manager_id=queue_manager.id,
        )

    db.session.add(new_risk_classification)
    db.session.commit()

    change_patient_queue(
        {
            "patient_id": patient_id,
            "queue_id": 2,
            "professional_id": professional_id,
        }
    )


def update_risk_classification(
    risk_classification_id: int, data: dict[str, str]
) -> None:

    risk_classification = get_risk_classification(
        risk_classification_id=risk_classification_id
    )

    risk_classification.weight = data.get("weight")
    risk_classification.sys_blood_pressure = data.get("sys_blood_pressure")
    risk_classification.dia_blood_pressure = data.get("dia_blood_pressure")
    risk_classification.temperature = data.get("temperature")
    risk_classification.heart_pulse = data.get("heart_pulse")
    risk_classification.diabetic = data.get("diabetic")
    risk_classification.fasting = data.get("fasting")
    risk_classification.professional_avaliation = data.get("professioal_avaliation")
    risk_classification.risk_classification = data.get("risk_classification")
    risk_classification.eye_opening = data.get("eye_opening")
    risk_classification.verbal_response = data.get("verbal_response")
    risk_classification.motor_response = data.get("motor_response")
    risk_classification.pupillary_reactivity = data.get("pupillary_reactivity")

    if "height" in data:
        risk_classification.height = data.get("height")

    if "respiratory_frequence" in data:
        risk_classification.respiratory_frequence = data.get("respiratory_frequence")

    if "capillary_blood_glucose" in data:
        risk_classification.capillary_blood_glucose = data.get(
            "capillary_blood_glucose"
        )

    db.session.commit()


def get_risk_classification(
    risk_classification_id: int, options: list = None
) -> RiskClassification:

    query = RiskClassification.query

    if options is not None:
        query = query.options(*options)

    risk_classification = query.get(risk_classification_id)

    if risk_classification is None:
        raise DefaultException("risk_classification_not_found", code=404)

    return risk_classification


from app.main.service.patient_service import get_patient
from app.main.service.professional_service import get_professional
from app.main.service.queue_manager_service import change_patient_queue
