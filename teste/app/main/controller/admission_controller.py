from flask import request
from flask_restx import Resource

from app.main.config import Config
from app.main.service import get_admissions, save_new_admission
from app.main.util import AdmissionDTO, DefaultResponsesDTO

admission_ns = AdmissionDTO.api
api = admission_ns
_admission_post = AdmissionDTO.admission_post
_admission_list = AdmissionDTO.admission_list
_default_message_response = DefaultResponsesDTO.message_response
_validation_error_response = DefaultResponsesDTO.validation_error

_CONTENT_PER_PAGE = Config.CONTENT_PER_PAGE
_DEFAULT_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


@api.route("")
class Admission(Resource):
    @api.doc("Admit patient")
    @api.expect(_admission_post, validate=True)
    @api.response(201, "patient_admitted", _default_message_response)
    @api.response(400, "Input payload validation failed", _validation_error_response)
    @api.response(
        404,
        "patient_not_found\nprofessional_not_found\nbed_not_found",
        _default_message_response,
    )
    @api.response(
        409,
        "bed_not_available\npatient_not_in_queue",
        _default_message_response,
    )
    def post(self) -> tuple[dict[str, str], int]:
        """Create a new patient admission"""
        data = request.json
        save_new_admission(data=data)
        return {"message": "patient_admitted"}, 201

    @api.doc(
        "List admissions",
        params={
            "page": {"description": "Page number", "default": 1, "type": int},
            "per_page": {
                "description": "Items per page",
                "default": _DEFAULT_CONTENT_PER_PAGE,
                "enum": _CONTENT_PER_PAGE,
                "type": int,
            },
            "patient_id": {"description": "Patient id", "type": int},
            "admission_id": {"description": "Admission id", "type": int},
            "bed_id": {"description": "Bed id", "type": int},
        },
        description=f"List of admissions with pagination. {_DEFAULT_CONTENT_PER_PAGE} admissions per page.",
    )
    @api.marshal_with(_admission_list, code=200, description="List of admissions")
    def get(self) -> tuple[dict[str, any], int]:
        """List registered admissions with pagination"""
        params = request.args
        return get_admissions(params=params)
