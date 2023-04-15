from flask_restx import Namespace, fields

from app.main.service import CustomDateTime


class VitalSignsControlDTO:
    api = Namespace(
        "vital_signs_control", description="vital signs control related operations"
    )

    vital_signs_control_without_performed_at = api.model(
        "vital_signs_control_without_performed_at",
        {
            "sys_blood_pressure": fields.Integer(
                description="patient systolic blood pressure",
                required=True,
                example=120,
            ),
            "dia_blood_pressure": fields.Integer(
                description="patient diastolic blood pressure",
                required=True,
                example=80,
            ),
            "heart_pulse": fields.Integer(
                description="patient heart pulse", required=True, example=70
            ),
            "respiratory_frequence": fields.Integer(
                description="patient respiratory frequence", required=True, example=15
            ),
            "body_fat_rate": fields.Integer(
                description="patient body fat rate (%)", example=15, required=True
            ),
            "temperature": fields.Float(
                description="patient temperature (ºC)", example=36.5
            ),
            "oxygen_saturation": fields.Integer(
                description="patient oxygen saturation", example=98
            ),
        },
    )

    vital_signs_control = api.clone(
        "vital_signs_control",
        vital_signs_control_without_performed_at,
        {
            "performed_at": CustomDateTime(description="time performed", required=True),
        },
    )
