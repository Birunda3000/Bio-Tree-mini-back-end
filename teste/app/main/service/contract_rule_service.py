import re
from math import ceil

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from sqlalchemy.dialects.postgresql import insert
from werkzeug.datastructures import ImmutableMultiDict

from app.main import db
from app.main.config import Config
from app.main.exceptions import DefaultException, ValidationException
from app.main.model import ContractRule

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def get_contract_rules(params: ImmutableMultiDict):

    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)
    description = params.get("description", type=str)

    filters = []

    if description:
        filters.append(ContractRule.description.ilike(f"%{description}%"))

    pagination = (
        ContractRule.query.filter(*filters)
        .order_by(ContractRule.id)
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return {
        "current_page": page,
        "total_items": pagination.total,
        "total_pages": ceil(pagination.total / per_page),
        "items": pagination.items,
    }


def save_new_contract_rule(data: dict[str, any]) -> None:

    code = data.get("code")
    contract_rule_type = data.get("type")

    if _contract_rule_exists(contract_rule_code=code):
        raise DefaultException("code_in_use", code=409)

    _validate_contract_rule_type(
        contract_rule_code=code, contract_rule_type=contract_rule_type
    )

    new_contract_rule = ContractRule(
        code=code,
        description=data.get("description"),
        ordinance=data.get("ordinance"),
        type=contract_rule_type,
    )

    db.session.add(new_contract_rule)
    db.session.commit()


def update_contract_rule(contract_rule_id: int, data: dict[str, str]) -> None:

    code = data.get("code")
    contract_rule_type = data.get("type")

    contract_rule = get_contract_rule(contract_rule_id=contract_rule_id)

    if _contract_rule_exists(
        contract_rule_code=code, contract_rule_id=contract_rule_id
    ):
        raise DefaultException("code_in_use", code=409)

    _validate_contract_rule_type(
        contract_rule_code=code, contract_rule_type=contract_rule_type
    )

    contract_rule.code = code
    contract_rule.description = data.get("description")
    contract_rule.ordinance = data.get("ordinance")
    contract_rule.type = contract_rule_type

    db.session.commit()


def delete_contract_rule(contract_rule_id: int):

    contract_rule = get_contract_rule(contract_rule_id=contract_rule_id)

    db.session.delete(contract_rule)
    db.session.commit()


def get_contract_rule(contract_rule_id: int, options: list = None) -> ContractRule:

    query = ContractRule.query

    if options is not None:
        query = query.options(*options)

    contract_rule = query.get(contract_rule_id)

    if contract_rule is None:
        raise DefaultException("contract_rule_not_found", code=404)

    return contract_rule


def import_contract_rules(data: dict[str, str]):
    url = data.get("url")
    ordinance = data.get("ordinance")

    response = requests.get(url)

    if response.status_code != 200:
        raise ValidationException(
            errors={"url": f"invalid url, returned code {response.status_code}"},
            message="Input payload validation failed",
            code=400,
        )

    soup = BeautifulSoup(response.text, "html.parser")

    table_rows = soup.select("tr")

    for table_row in table_rows:
        if table_row.find(["s", "th"]):
            continue

        table_columns = table_row.find_all("td")

        if not re.match(r"^[0-9]{2}.[0-9]{2}$", table_columns[0].text.strip()):
            continue

        _upsert_contract_rules_by_table_column(
            table_columns=table_columns, ordinance=ordinance
        )

    db.session.commit()


def _upsert_contract_rules_by_table_column(
    table_columns: list[Tag], ordinance: str
) -> None:
    upsert_stmt = insert(ContractRule).values(
        code=table_columns[0].text.strip(),
        description=table_columns[1].text.strip(),
        ordinance=ordinance,
        type=table_columns[2].text.strip() if len(table_columns) == 3 else None,
    )

    upsert_stmt = upsert_stmt.on_conflict_do_update(
        index_elements=["code"],
        set_={
            "description": upsert_stmt.excluded.description,
            "ordinance": upsert_stmt.excluded.ordinance,
            "type": upsert_stmt.excluded.type,
        },
    )

    db.session.execute(upsert_stmt)


def _contract_rule_exists(
    contract_rule_code: str, contract_rule_id: int = None
) -> bool:

    filters = [ContractRule.code == contract_rule_code]

    if contract_rule_id:
        filters.append(ContractRule.id != contract_rule_id)

    return (
        ContractRule.query.with_entities(ContractRule.id).filter(*filters).scalar()
        is not None
    )


def _validate_contract_rule_type(
    contract_rule_code: str, contract_rule_type: str
) -> None:
    if (
        not re.match(r"^[0-9]{2}.00$", contract_rule_code)
        and contract_rule_type is None
    ):
        raise ValidationException(
            errors={
                "type": "'type' is a required property if code does not end with .00"
            },
            message="Input payload validation failed",
            code=400,
        )
