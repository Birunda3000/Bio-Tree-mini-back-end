from flask_restx import Namespace, fields

from app.main.enum import *
from app.main.service import CustomDate, CustomDateTime
from app.main.util.fces import FcesDTO


class ProfessionalBondDTO:
    api = Namespace(
        "professional_bond", description="professional bond related operations"
    )

    professional_bond_id = {"id": fields.Integer(description="professional bond id")}

    fces_id = {"fces_id": fields.Integer(required=True, description="fces id")}

    professional_id = {
        "professional_id": fields.Integer(required=True, description="professional id")
    }

    preceptor_professional_id = {
        "preceptor_professional_id": fields.Integer(
            required=True, description="preceptor professional id"
        )
    }

    occupation_id = {
        "occupation_id": fields.Integer(required=True, description="occupation id")
    }

    contract_type = {
        "contract_type": fields.String(required=True, description="contract type"),
    }

    contract_number = {
        "contract_number": fields.String(required=True, description="contract number"),
    }

    edict_number = {
        "edict_number": fields.String(required=True, description="edict number"),
    }

    type_of_bond = {
        "type_of_bond": fields.String(
            required=True, description="type of bond", enum=BOND_OPTIONS
        ),
    }

    contract_start = {
        "contract_start": CustomDate(required=True, description="contract start"),
    }

    contract_end = {
        "contract_end": CustomDate(required=True, description="contract end"),
    }

    workload_ambulance = {
        "workload_ambulance": CustomDateTime(
            required=True, description="workload ambulance"
        ),
    }

    workload_hospital = {
        "workload_hospital": CustomDateTime(
            required=True, description="workload hospital"
        ),
    }

    workload_others = {
        "workload_others": CustomDateTime(required=True, description="workload others"),
    }

    attends_sus = {
        "attends_sus": fields.Boolean(required=True, description="attends sus"),
    }

    attends_apac = {
        "attends_apac": fields.Boolean(required=True, description="attends apac"),
    }

    employer_cnpj = {
        "employer_cnpj": fields.String(required=True, description="employer cnpj"),
    }

    legal_nature = {
        "legal_nature": fields.String(required=True, description="legal nature"),
    }

    occupation = {
        "id": fields.Integer(description="occupation id"),
        "name": fields.String(description="occupation name"),
    }

    professional_bond_post = api.model(
        "professional_bond_post",
        fces_id
        | professional_id
        | preceptor_professional_id
        | occupation_id
        | contract_type
        | contract_number
        | edict_number
        | type_of_bond
        | contract_start
        | contract_end
        | workload_ambulance
        | workload_hospital
        | workload_others
        | attends_sus
        | attends_apac
        | employer_cnpj
        | legal_nature,
    )

    professional_bond_response = api.model(
        "professional_bond_response",
        professional_bond_id
        | contract_type
        | contract_number
        | edict_number
        | type_of_bond
        | contract_start
        | contract_end
        | workload_ambulance
        | workload_hospital
        | workload_others
        | attends_sus
        | attends_apac
        | employer_cnpj
        | legal_nature
        | {
            "fces": fields.Nested(
                api.model(
                    "professional_bond_response_occupation",
                    FcesDTO.fces_id | FcesDTO.fces_corporate_name,
                )
            )
        }
        | {
            "occupation": fields.Nested(
                api.model("professional_bond_response_occupation", occupation)
            )
        },
    )

    professional_bond_list = api.model(
        "professional_bond_list",
        {
            "current_page": fields.Integer(),
            "total_items": fields.Integer(),
            "total_pages": fields.Integer(),
            "items": fields.List(fields.Nested(professional_bond_response)),
        },
    )
