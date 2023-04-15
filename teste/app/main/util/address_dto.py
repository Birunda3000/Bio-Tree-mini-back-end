from ..enum import STATES_OPTIONS
from flask_restx import Namespace, fields


class AddressDTO:
    api = Namespace("address", description="address related operations")

    address = api.model(
        "address",
        {
            "cep": fields.String(
                required=True,
                description="address cep",
                min_length=8,
                max_length=8,
                pattern="^[0-9]{8}$",
                example="68911466",
            ),

            "state": fields.String(required=True, description="address state", enum=STATES_OPTIONS),# address_UF
            
            #logradouro??
            
            "district": fields.String(required=True, description="address district"),

            "city": fields.String(required=True, description="address city"),

            "number": fields.String(required=True, description="address number", example="123"),

            "complement": fields.String(
                required=True, description="address complement"
            ),

            "street": fields.String(required=True, description="address street"),

        },
    )
