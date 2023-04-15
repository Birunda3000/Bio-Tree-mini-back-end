from flask_restx import Namespace, fields

from app.main.service import CustomDateTime
from app.main.util.vital_signs_control_dto import VitalSignsControlDTO

_vital_signs_control = VitalSignsControlDTO.vital_signs_control_without_performed_at


class HistoryNursingPrescriptionVitalSignsControlDTO:
    api = Namespace(
        "history_nursing_prescription_vital_signs_control",
        description="history nursing prescription vitalsignscontrol related operations",
    )

    history_nursing_prescription_vitalsignscontrol = api.model(
        "history_nursing_prescription_vital_signs_control",
        {
            "vital_signs_control": fields.Nested(_vital_signs_control),
            "performed_at": CustomDateTime(
                description="vital signs control performed date and time",
            ),
        },
    )
