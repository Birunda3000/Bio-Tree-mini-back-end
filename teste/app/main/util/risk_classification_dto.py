from flask_restx import Namespace, fields

from app.main.model import (
    EYE_OPENING,
    MOTOR_RESPONSE,
    PUPILLARY_REACTIVITY,
    RISK_CLASSIFICATIONS,
    VERBAL_RESPONSE,
)


class RiskClassificationDTO:

    api = Namespace(
        "risk classification", description="risk classification related operations"
    )

    risk_classification_put = api.model(
        "risk_classification_update",
        {
            "weight": fields.Float(
                description="patient weight", example=60.005, required=True
            ),
            "height": fields.Float(description="patient height", example=1.70),
            "sys_blood_pressure": fields.Integer(
                description="patient systolic blood pressure",
                example=120,
                required=True,
            ),
            "dia_blood_pressure": fields.Integer(
                description="patient diastolic blood pressure",
                example=80,
                required=True,
            ),
            "temperature": fields.Float(
                description="patient temperature (ºC)", example=36.5, required=True
            ),
            "heart_pulse": fields.Integer(
                description="patient heart pulse", example=70, required=True
            ),
            "respiratory_frequence": fields.Integer(
                description="patient respiratory frequence", example=15
            ),
            "diabetic": fields.Boolean(description="patient diabetic", default=False),
            "capillary_blood_glucose": fields.Integer(
                description="patient capillary blood glucose", example=75
            ),
            "eye_opening": fields.String(
                description="patient eye opening", enum=EYE_OPENING
            ),
            "verbal_response": fields.String(
                description="patient verbal response", enum=VERBAL_RESPONSE
            ),
            "motor_response": fields.String(
                description="patient motor response", enum=MOTOR_RESPONSE
            ),
            "pupillary_reactivity": fields.String(
                description="patient pupillary reactivity", enum=PUPILLARY_REACTIVITY
            ),
            "fasting": fields.Boolean(description="patient fasting", default=True),
            "professional_avaliation": fields.String(
                description="professional avaliation", max_length=500
            ),
            "risk_classification": fields.String(
                description="patient risk_classification",
                enum=RISK_CLASSIFICATIONS,
                required=True,
            ),
        },
    )

    risk_classification_post = api.clone(
        "risk_classification_create",
        {
            "weight": fields.Float(description="patient weight", example=60.005),
            "height": fields.Float(description="patient height", example=1.70),
            "sys_blood_pressure": fields.Integer(
                description="patient systolic blood pressure",
                example=120,
            ),
            "dia_blood_pressure": fields.Integer(
                description="patient diastolic blood pressure",
                example=80,
            ),
            "temperature": fields.Float(
                description="patient temperature (ºC)", example=36.5
            ),
            "heart_pulse": fields.Integer(
                description="patient heart pulse", example=70
            ),
            "respiratory_frequence": fields.Integer(
                description="patient respiratory frequence", example=15
            ),
            "diabetic": fields.Boolean(description="patient diabetic", default=False),
            "capillary_blood_glucose": fields.Integer(
                description="patient capillary blood glucose", example=75
            ),
            "eye_opening": fields.String(
                description="patient eye opening", enum=EYE_OPENING
            ),
            "verbal_response": fields.String(
                description="patient verbal response", enum=VERBAL_RESPONSE
            ),
            "motor_response": fields.String(
                description="patient motor response", enum=MOTOR_RESPONSE
            ),
            "pupillary_reactivity": fields.String(
                description="patient pupillary reactivity", enum=PUPILLARY_REACTIVITY
            ),
            "fasting": fields.Boolean(description="patient fasting", default=True),
            "professional_avaliation": fields.String(
                description="professional avaliation", max_length=500
            ),
            "risk_classification": fields.String(
                description="patient risk_classification",
                enum=RISK_CLASSIFICATIONS,
                required=True,
            ),
            "patient_id": fields.Integer(
                description="patient relationship", required=True, example=1
            ),
            "professional_id": fields.Integer(
                description="professional relationship", required=True, example=1
            ),
        },
    )

    risk_classification_response = api.clone(
        "risk_classification_response",
        risk_classification_post,
        {"id": fields.Integer(description="risk classification id")},
    )

    risk_classification_history = api.model(
        "risk_classification_history",
        {
            "current_page": fields.Integer(),
            "total_items": fields.Integer(),
            "total_pages": fields.Integer(),
            "items": fields.List(fields.Nested(risk_classification_response)),
        },
    )
