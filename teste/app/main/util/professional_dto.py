from flask_restx import Namespace, fields

from app.main.enum import *
from app.main.service import CPF, CustomDatePast, Email
from app.main.util.address_dto import AddressDTO
from app.main.util.professional_bond_dto import ProfessionalBondDTO

_address = AddressDTO.address


class ProfessionalDTO:
    api = Namespace("professional", description="professional related operations")

    professional_id = {"id": fields.Integer(description="professional id")}
    # Dados principais
    professional_name = {
        "name": fields.String(
            required=True, description="professional name", min_length=1
        ),
    }

    professional_social_name = {
        "social_name": fields.String(description="professional social name"),
    }

    professional_cpf = {
        "cpf": CPF(required=True, description="professional cpf", example="86493602033")
    }

    professional_cns_cod = {
        "cns_cod": fields.String(
            description="professional CNS code",
            min_length=15,
            max_length=15,
        )
    }

    professional_birth = {
        "birth": CustomDatePast(required=False, description="professional birth date")
    }

    professional_breed = {
        "breed": fields.String(
            required=False,
            description="professional breed",
            enum=BREED_OPTIONS,
        )
    }

    professional_gender = {
        "gender": fields.String(
            required=False,
            description="professional gender",
            enum=GENDER_OPTIONS,
        )
    }

    professional_sex = {
        "sex": fields.String(
            required=False,
            description="professional sex",
            enum=SEX_OPTIONS,
        )
    }

    professional_mother_name = {
        "mother_name": fields.String(
            required=False, description="professional mother name"
        )
    }

    professional_father_name = {
        "father_name": fields.String(
            required=False,
            description="professional father name",
        ),
    }

    professional_education = {
        "education": fields.String(
            required=False,
            description="professional education",
            enum=EDUCATION_OPTIONS,
        )
    }

    professional_nationality = {
        "nationality": fields.String(
            required=False,
            description="professional nationality",
            enum=NATIONALITY_OPTIONS,
        )
    }

    professional_country = {
        "country": fields.String(required=False, description="professional country")
    }

    professional_FU_of_nationality = {
        "FU_of_nationality": fields.String(
            required=False,
            description="professional FU of nationality",
            enum=STATES_OPTIONS,
        )
    }

    professional_citizenship = {
        "citizenship": fields.String(
            required=False,
            description="professional citizenship",
        )
    }  # cidade API

    date_of_entry = {
        "date_of_entry": CustomDatePast(
            required=False,
            description="professional date of entry",
        )
    }

    date_of_naturalization = {
        "date_of_naturalization": CustomDatePast(
            required=False,
            description="professional date of naturalization",
        )
    }

    # address

    professional_email = {
        "email": Email(
            required=False, description="professional mail", example="12345@gmail.com"
        )
    }

    professional_ddi = {
        "ddi": fields.String(
            required=False,
            description="professional DDI",
            min_length=2,
            max_length=3,
        )
    }

    professional_emergency_phone = {
        "emergency_phone": fields.String(
            required=False,
            description="professional emergency phone",
            example="88911466",
        )
    }

    professional_bank_number = {
        "bank_number": fields.String(
            required=False,
            description="professional bank number",
        )
    }

    professional_bank_name = {
        "bank_name": fields.String(
            required=False,
            description="professional bank name",
        )
    }

    professional_agency_number = {
        "agency_number": fields.String(
            required=False,
            description="professional agency number",
        )
    }

    professional_current_account = {
        "current_account": fields.String(
            required=False,
            description="professional current account",
        )
    }
    professional_inactive = {
        "inactive": fields.Boolean(
            description="professional inactive",
        )
    }

    professional_address = {
        "address": fields.Nested(
            _address,
            required=False,
        )
    }

    professional_dismissal_cause = {
        "dismissal_cause": fields.String(
            required=True,
            description="professional dismissal cause",
            enum=DISMISSAL_CAUSE_OPTIONS,
        )
    }




    professional_bond = {}

    professional_post = api.model(
        "professional_create",
        professional_name
        | professional_social_name
        | professional_cpf
        | professional_cns_cod
        | professional_birth
        | professional_breed
        | professional_gender
        | professional_sex
        | professional_mother_name
        | professional_father_name
        | professional_education
        | professional_nationality
        | professional_country
        | professional_FU_of_nationality
        | professional_citizenship
        | date_of_entry
        | date_of_naturalization
        | professional_email
        | professional_ddi
        | professional_emergency_phone
        | professional_bank_number
        | professional_bank_name
        | professional_agency_number
        | professional_current_account
        | professional_address
        | {
            "professional_bonds": fields.List(
                fields.Nested(ProfessionalBondDTO.professional_bond_response)
            )
        },
    )

    professional_response = api.clone(
        "professional_response",
        professional_id,
        professional_post,
    )

    professional_list = api.model(
        "professional_list",
        {
            "current_page": fields.Integer(),
            "total_items": fields.Integer(),
            "total_pages": fields.Integer(),
            "items": fields.List(fields.Nested(professional_response)),
        },
    )

    professional_by_name = api.model(
        "professional_by_name",
        professional_id | professional_name | professional_social_name,
    )

    professional_inactivation = api.model(
        "professional_inactivation",
        professional_dismissal_cause,
    )