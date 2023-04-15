from flask_restx import Namespace, fields

from app.main.service import CustomDateTimePast, CustomDateTime
from app.main.util.cid_10_dto import Cid10DTO
from app.main.util.patient_dto import PatientDTO
from app.main.util.professional_dto import ProfessionalDTO

_cid_10_response = Cid10DTO.cid_10_response


class DeathLaunchDTO:
    api = Namespace("death_launch", description="death launch related operations")

    death_launch_post = api.model(
        "death_launch_post",
        {
            "patient_id": fields.Integer(
                required=True, description="patient relationship"
            ),
            "professional_id": fields.Integer(
                required=True, description="professional relationship"
            ),
            "cid_10_id": fields.Integer(
                required=True, description="cid 10 relationship"
            ),
            "certificate_number": fields.Integer(
                required=True, description="certificate number"
            ),
            "place": fields.String(required=True, description="place of death"),
            "circunstances_of_death": fields.String(
                description="circusntances of death"
            ),
            "datetime_of_death": CustomDateTimePast(
                required=True,
                description="date and time of death",
            ),
            "registration_datetime": CustomDateTimePast(
                required=True,
                description="registration of death date and time",
            ),
        },
    )

    death_launch_put = api.model(
        "death_launch_put",
        {
            "professional_id": fields.Integer(
                required=True, description="professional relationship"
            ),
            "cid_10_id": fields.Integer(
                required=True, description="cid 10 relationship"
            ),
            "certificate_number": fields.Integer(
                required=True, description="certificate number"
            ),
            "place": fields.String(required=True, description="place of death"),
            "circunstances_of_death": fields.String(
                description="circunstances of death"
            ),
            "datetime_of_death": CustomDateTimePast(
                required=True,
                description="date and time of death",
            ),
            "registration_datetime": CustomDateTimePast(
                required=True,
                description="registration of death date and time",
            ),
        },
    )

    death_launch_response = api.model(
        "death_launch_response",
        {
            "id": fields.Integer(description="death launch id"),
            "cid_10": fields.Nested(
                _cid_10_response, description="cid 10 relationship"
            ),
            "patient": fields.Nested(
                api.model(
                    "patient_death_launch_response",
                    PatientDTO.patient_id
                    | PatientDTO.patient_name
                    | PatientDTO.patient_social_name
                    | PatientDTO.patient_sex
                    | PatientDTO.patient_birth,
                ),
                description="patient relationship",
            ),
            "professional": fields.Nested(
                api.model(
                    "professional_death_launch_response",
                    ProfessionalDTO.professional_id
                    | ProfessionalDTO.professional_social_name
                    | ProfessionalDTO.professional_name,
                ),
                description="professional relationship",
            ),
            "certificate_number": fields.Integer(description="certificate number"),
            "circunstances_of_death": fields.String(
                description="circusntances of death"
            ),
            "place": fields.String(description="place of death"),
            "datetime_of_death": CustomDateTime(
                description="date and time of death",
            ),
            "registration_datetime": CustomDateTime(
                description="registration of death date and time",
            ),
        },
    )

    death_launch_response_by_list = api.model(
        "death_launch_response_by_list",
        {
            "id": fields.Integer(description="death launch id"),
            "name": fields.String(
                description="patient name. Social name if patient has social name"
            ),
            "responsible_for_registration": fields.String(
                description="responsible for registration"
            ),
            "datetime_of_death": CustomDateTime(
                description="date and time of death",
            ),
            "registration_datetime": CustomDateTime(
                description="registration of death date and time",
            ),
        },
    )

    death_launch_list = api.model(
        "death_launch_list",
        {
            "current_page": fields.Integer(),
            "total_items": fields.Integer(),
            "total_pages": fields.Integer(),
            "items": fields.List(fields.Nested(death_launch_response_by_list)),
        },
    )
