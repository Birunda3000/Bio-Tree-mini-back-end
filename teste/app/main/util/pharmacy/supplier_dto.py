from flask_restx import Namespace, fields

from app.main.service import CNPJ, CPF


class SupplierDTO:
    api = Namespace("supplier", description="supplier related operations")

    supplier_id = {"id": fields.Integer(description="supplier id")}

    supplier_name = {
        "name": fields.String(required=True, description="supplier name", min_length=1)
    }

    supplier_cpf = {"cpf": CPF(required=True, description="supplier cpf")}

    supplier_cnpj = {"cnpj": CNPJ(required=True, description="supplier cnpj")}

    supplier_post_natural_person = api.model(
        "supplier_post_natural_person", supplier_name | supplier_cpf
    )

    supplier_post_legal_person = api.model(
        "supplier_post_legal_person", supplier_name | supplier_cnpj
    )

    supplier_update = api.model("supplier_put", supplier_name)

    supplier_response = api.clone(
        "supplier_response", supplier_id, supplier_name | supplier_cpf | supplier_cnpj
    )

    supplier_list = api.model(
        "supplier_list",
        {
            "current_page": fields.Integer(),
            "total_items": fields.Integer(),
            "total_pages": fields.Integer(),
            "items": fields.List(fields.Nested(supplier_response)),
        },
    )
