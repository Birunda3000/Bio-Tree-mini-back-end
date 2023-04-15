from flask_restx import Namespace, fields

from app.main.model import ADMISSION_TYPES
from app.main.service import CustomDateTime
from app.main.util.bed_dto import BedDTO

_bed_id_room = BedDTO.bed_id_room


class AdmissionDTO:

    api = Namespace("admission", description="admission related operations")

    admission_post = api.model(
        "admission_post",
        {
            "patient_id": fields.Integer(
                required=True, description="patient relationship", example=1
            ),
            "professional_id": fields.Integer(
                required=True, description="professional relationship", example=1
            ),
            "bed_id": fields.Integer(
                required=True, description="bed relationship", example=1
            ),
            "type": fields.String(
                required=True, description="admission type", enum=ADMISSION_TYPES
            ),
        },
    )

    admission_response = api.model(
        "admission_response",
        {
            "id": fields.Integer(description="admission id"),
            "patient_id": fields.Integer(
                required=True, description="patient relationship", example=1
            ),
            "professional_id": fields.Integer(
                required=True, description="professional relationship", example=1
            ),
            "bed": fields.Nested(_bed_id_room),
            "type": fields.String(
                required=True, description="admission type", enum=ADMISSION_TYPES
            ),
            "admitted_at": CustomDateTime(
                required=True,
                description="admission date and time",
            ),
        },
    )

    admission_list = api.model(
        "admission_list",
        {
            "current_page": fields.Integer(),
            "total_items": fields.Integer(),
            "total_pages": fields.Integer(),
            "items": fields.List(fields.Nested(admission_response)),
        },
    )
