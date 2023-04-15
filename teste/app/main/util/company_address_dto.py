from flask_restx import Namespace, fields


class CompanyAddressDTO:
    api = Namespace("company_address", description="company address related operations")

    company_address = api.model(
        "company_address",
        {
            "street": fields.String(
                required=True, description="company address street"
            ),
            "district": fields.String(
                required=True, description="company address district"
            ),
            "city": fields.String(required=True, description="company address city"),
            "state": fields.String(required=True, description="company address state"),
            "complement": fields.String(
                required=True, description="company address complement"
            ),
            "number": fields.String(
                required=True, description="company address number"
            ),
            "cep": fields.String(
                required=True,
                description="company address cep",
                min_length=8,
                max_length=8,
                pattern="^[0-9]{8}$",
                example="68911466",
            ),
            "municipality": fields.String(
                required=True, description="company address municipality"
            ),
            "latitude": fields.Float(
                required=True, description="company address latitude", example=3.727380
            ),
            "longitude": fields.Float(
                required=True,
                description="company address longitude",
                example=38.570772,
            ),
            "sanitary_district_id": fields.Integer(
                required=True, description="company address sanitary district relationship"
            ),
            "regional_health": fields.String(
                required=True, description="company address regional health"
            ),
            "microregion": fields.String(
                required=True, description="company address microregion"
            ),
            "assistance_module": fields.String(
                required=True, description="company address assistance module"
            ),
        },
    )
