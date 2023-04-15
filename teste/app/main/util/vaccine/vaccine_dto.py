from flask_restx import Namespace, fields

from app.main.util.vaccine.vaccine_laboratory_dto import VaccineLaboratoryDTO

_laboratory_response = VaccineLaboratoryDTO.vaccine_laboratory_response


class VaccineDTO:

    api = Namespace("vaccine", description="vaccine related operations")

    vaccine_id = {"id": fields.Integer(description="vaccine id")}
    vaccine_name = {
        "name": fields.String(required=True, description="vaccine name", min_length=1)
    }
    vaccine_pni_code = {
        "pni_code": fields.String(required=True, description="vaccine PNI code")
    }
    vaccine_belongs_to_vaccine_card = {
        "belongs_to_vaccine_card": fields.Boolean(
            required=True, description="true if vaccine belongs to vaccine card"
        )
    }
    vaccine_current = {
        "current": fields.Boolean(
            required=True, description="true if vaccine is current"
        )
    }
    vaccine_export_to_esus = {
        "export_to_esus": fields.Boolean(
            required=True, description="true if vaccine should be export to esus"
        )
    }
    vaccine_controls_vaccine_batch = {
        "controls_vaccine_batch": fields.Boolean(
            required=True, description="true if vaccine is controls vaccine batch"
        )
    }
    vaccine_oblige_establishment = {
        "oblige_establishment": fields.Boolean(
            required=True,
            description="true if vaccine is oblige CNES/establishment at rescue",
        )
    }
    vaccine_laboratory_ids = {
        "laboratory_ids": fields.List(
            fields.Integer(description="vaccine laboratory id"),
            required=True,
            description="vaccine laboratory id list",
            min_items=1,
        )
    }

    vaccine_post = api.model(
        "vaccine_create",
        vaccine_name
        | vaccine_pni_code
        | vaccine_belongs_to_vaccine_card
        | vaccine_current
        | vaccine_export_to_esus
        | vaccine_controls_vaccine_batch
        | vaccine_oblige_establishment
        | vaccine_laboratory_ids,
    )

    vaccine_update = api.clone("vaccine_put", vaccine_post)

    vaccine_response = api.model(
        "vaccine_response",
        vaccine_id
        | vaccine_name
        | vaccine_pni_code
        | vaccine_belongs_to_vaccine_card
        | vaccine_current
        | vaccine_export_to_esus
        | vaccine_controls_vaccine_batch
        | vaccine_oblige_establishment
        | {
            "laboratories": fields.List(
                fields.Nested(_laboratory_response, description="laboratory data"),
                description="vaccine laboratories relationship",
            )
        },
    )

    vaccine_by_name = api.model("vaccine_by_name", vaccine_id | vaccine_name)

    vaccine_list = api.model(
        "vaccine_list",
        {
            "current_page": fields.Integer(),
            "total_items": fields.Integer(),
            "total_pages": fields.Integer(),
            "items": fields.List(fields.Nested(vaccine_by_name)),
        },
    )
