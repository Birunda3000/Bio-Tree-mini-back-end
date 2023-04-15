from flask_restx import Namespace, fields
from app.main.model import CONTRACT_RULE_OPTIONS


class ContractRuleDTO:
    api = Namespace("contract_rule", description="contract rule related operations")

    contract_rule_import = api.model(
        "contract_rule_import",
        {
            "url": fields.String(
                descrption="contract rule site url",
                pattern=r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)",
                example="https://bvsms.saude.gov.br/bvs/saudelegis/sas/2009/prt0329_06_10_2009.html",
                required=True,
            ),
            "ordinance": fields.String(
                description="contract rules ordinance",
                min_length=1,
                example="399/GM",
                required=True,
            ),
        },
    )

    contract_rule_post = api.model(
        "contract_rule_post",
        {
            "code": fields.String(
                description="contract rule code",
                min_length=1,
                required=True,
            ),
            "description": fields.String(
                description="contract rule description",
                min_length=1,
                required=True,
            ),
            "ordinance": fields.String(
                description="contract rule ordinance",
                min_length=1,
                required=True,
            ),
            "type": fields.String(
                description="contract rule type", enum=CONTRACT_RULE_OPTIONS
            ),
        },
    )

    contract_rule_update = api.clone("contract_rule_put", contract_rule_post)

    contract_rule_response = api.clone(
        "contract_rule_response",
        {"id": fields.Integer(description="contract rule id")},
        contract_rule_post,
    )

    contract_rule_list = api.model(
        "contract_rule_list",
        {
            "current_page": fields.Integer(),
            "total_items": fields.Integer(),
            "total_pages": fields.Integer(),
            "items": fields.List(fields.Nested(contract_rule_response)),
        },
    )
