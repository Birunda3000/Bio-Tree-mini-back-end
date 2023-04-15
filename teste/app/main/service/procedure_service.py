from math import ceil

import pdfplumber
from sqlalchemy.dialects.postgresql import insert
from werkzeug.datastructures import FileStorage, ImmutableMultiDict

from app.main import db
from app.main.config import Config
from app.main.exceptions import DefaultException, ValidationException
from app.main.model import Procedure

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def get_procedures(params: ImmutableMultiDict):

    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)
    code = params.get("code", type=str)
    show_inactivated = params.get("show_inactivated", type=str, default="false").upper()
    description = params.get("description", type=str)
    classification = params.get("classification", type=str)

    filters = []

    if code:
        filters.append(Procedure.code.like(f"%{code}%"))
    if description:
        filters.append(Procedure.description.ilike(f"%{description}%"))
    if classification:
        filters.append(Procedure.classification.like(f"%{classification}%"))

    if show_inactivated == "FALSE":
        filters.append(Procedure.active.is_(True))

    pagination = (
        Procedure.query.filter(*filters)
        .order_by(Procedure.id)
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return {
        "current_page": page,
        "total_items": pagination.total,
        "total_pages": ceil(pagination.total / per_page),
        "items": pagination.items,
    }


def upsert_procedures(file: FileStorage):
    if file.content_type != "application/pdf":
        raise ValidationException(
            errors={"file": "The file type must be PDF"}, message="invalid_type_file"
        )

    with pdfplumber.open(file) as pdf:

        # Remove title and header
        first_page = pdf.pages[0]
        table = first_page.extract_table()[2:]

        if len(table[0]) != 5:
            raise ValidationException(
                errors={"file": "The table must have 5 columns"},
                message="invalid_columns_file",
            )

        _upsert_procedures_by_table(table=table)

        # Other pages
        for number_page in range(1, len(pdf.pages)):
            table = pdf.pages[number_page].extract_table()
            _upsert_procedures_by_table(table=table)

        db.session.commit()


def _upsert_procedures_by_table(table: list[list[str]]) -> None:
    for row in table:
        upsert_stmt = insert(Procedure).values(
            code=row[0],
            classification=row[1],
            dv=row[2],
            description=row[3],
            price=row[4].replace(".", "").replace(",", "."),
        )

        # If "code" already exists, update procedure
        upsert_stmt = upsert_stmt.on_conflict_do_update(
            index_elements=["code"],
            set_={
                "classification": upsert_stmt.excluded.classification,
                "dv": upsert_stmt.excluded.dv,
                "description": upsert_stmt.excluded.description,
                "price": upsert_stmt.excluded.price,
            },
        )

        db.session.execute(upsert_stmt)


def inactivate_procedure(procedure_id: int) -> None:
    procedure = get_procedure(procedure_id=procedure_id)

    procedure.active = False

    db.session.commit()


def activate_procedure(procedure_id: int) -> None:
    procedure = get_procedure(procedure_id=procedure_id, inactive_check=False)

    if procedure.active:
        raise DefaultException("procedure_is_active", code=409)

    procedure.active = True

    db.session.commit()


def get_procedure(
    procedure_id: int, options: list = None, inactive_check: bool = True
) -> Procedure:

    query = Procedure.query

    if options is not None:
        query = query.options(*options)

    procedure = query.get(procedure_id)

    if procedure is None:
        raise DefaultException("procedure_not_found", code=404)

    if inactive_check and not procedure.active:
        raise DefaultException("procedure_is_inactive", code=409)

    return procedure
