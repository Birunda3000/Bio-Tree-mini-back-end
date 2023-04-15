from flask_restx import Namespace, fields

from ..enum import *
from app.main.service import CPF, CustomDate, CustomDatePast, Email
from app.main.util.address_dto import AddressDTO
from app.main.util.contact_dto import ContactDTO

_address = AddressDTO.address
_contact = ContactDTO.contact


class PatientDTO:
    api = Namespace("patient", description="patient related operations")

    patient_id = {"id": fields.Integer(description="patient id")}
    patient_name = {
        "name": fields.String(required=True, description="patient name", min_length=1)
    }
    patient_social_name = {
        "social_name": fields.String(description="patient social name")
    }
    patient_cpf = {"cpf": CPF(required=True, description="patient cpf")}
    patient_email = {"email": Email(description="patient mail")}
    patient_birth = {
        "birth": CustomDatePast(required=True, description="patient birth date")
    }
    patient_sex = {
        "sex": fields.String(required=True, description="patient sex", enum=SEX_OPTIONS)
    }
    patient_mother_name = {
        "mother_name": fields.String(required=True, description="patient mother name"),
    }
    patient_father_name = {
        "father_name": fields.String(description="patient father name")
    }
    patient_cns_cod = {
        "cns_cod": fields.String(
            description="patient CNS code", min_length=15, max_length=15
        )
    }
    patient_gender = {
        "gender": fields.String(
            required=True, description="patient gender", enum=GENDER_OPTIONS
        )
    }
    patient_medical_number = {
        "medical_number": fields.Integer(
            required=True, description="patient medical number"
        )
    }
    patient_breed = {
        "breed": fields.String(
            required=True, description="patient breed", enum=BREED_OPTIONS
        )
    }
    patient_address = {"address": fields.Nested(_address)}
    patient_contact = {"contact": fields.Nested(_contact)}

    patient_post = api.model(
        "patient_create",
        patient_name
        | patient_social_name
        | patient_cpf
        | patient_email
        | patient_birth
        | patient_sex
        | patient_mother_name
        | patient_father_name
        | patient_cns_cod
        | patient_gender
        | patient_medical_number
        | patient_breed
        | patient_address
        | patient_contact,
    )

    patient_response = api.clone(
        "patient_response",
        patient_id,
        patient_post,
    )

    patient_list = api.model(
        "patient_list",
        {
            "current_page": fields.Integer(),
            "total_items": fields.Integer(),
            "total_pages": fields.Integer(),
            "items": fields.List(fields.Nested(patient_response)),
        },
    )

    patient_by_name = api.model(
        "patient_by_name", patient_id | patient_name | patient_social_name
    )
