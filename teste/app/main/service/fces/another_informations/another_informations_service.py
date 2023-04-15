from sqlalchemy import or_
from sqlalchemy.orm import joinedload

from app.main import db
from app.main.exceptions import DefaultException
from app.main.model import AnotherInformations


def save_new_another_informations(fces_id: int, data: dict[str, any]) -> None:

    sanitary_number = data.get("sanitary_number")
    leavings_selected = data.get("leavings_selected")
    commission_types_selected = data.get("commission_types_selected")

    fces = get_fces(fces_id=fces_id)

    _verify_unique_data(fces_id=fces_id, sanitary_number=sanitary_number)

    leavings = []
    if leavings_selected:
        leavings = validate_leavings(set(leavings_selected))

    commission_types = []
    if commission_types_selected:
        commission_types = validate_commission_types(set(commission_types_selected))

    new_another_informations = AnotherInformations(
        fces=fces,
        sanitary_number=sanitary_number,
        issuance_date=date_from_string(value=data.get("issuance_date")),
        issuing_agency=data.get("issuing_agency"),
        bank=data.get("bank"),
        agency=data.get("agency"),
        current_account=data.get("current_account"),
        administrative_field=data.get("administrative_field"),
        hierarchy_level=data.get("hierarchy_level"),
        teaching_research_activity_text=data.get("teaching_research_activity_text"),
        tax_withholding=data.get("tax_withholding"),
        service_shift=data.get("service_shift"),
        nature_organization=data.get("nature_organization"),
        attendance=data.get("attendance"),
        covenant=data.get("covenant"),
        leavings_selected=leavings,
        commission_types_selected=commission_types,
    )

    db.session.add(new_another_informations)
    db.session.commit()


def update_another_informations(fces_id: int, data: dict[str, str]) -> None:

    sanitary_number = data.get("sanitary_number")
    leavings_selected = data.get("leavings_selected")
    commission_types_selected = data.get("commission_types_selected")

    another_informations = get_another_informations(
        fces_id=fces_id, with_commissions_types_and_leavings_list=False
    )

    if another_informations.sanitary_number != sanitary_number:
        _verify_unique_data(
            fces_id=None,
            sanitary_number=sanitary_number,
            filters=[AnotherInformations.id != another_informations.id],
        )
        another_informations.sanitary_number = data.get("sanitary_number")

    if leavings_selected:
        leavings = validate_leavings(set(leavings_selected))
        another_informations.leavings_selected = leavings

    if commission_types_selected:
        commission_types = validate_commission_types(set(commission_types_selected))
        another_informations.commission_types_selected = commission_types

    another_informations.issuance_date = date_from_string(
        value=data.get("issuance_date")
    )
    another_informations.issuing_agency = data.get("issuing_agency")
    another_informations.bank = data.get("bank")
    another_informations.agency = data.get("agency")
    another_informations.current_account = data.get("current_account")
    another_informations.administrative_field = data.get("administrative_field")
    another_informations.hierarchy_level = data.get("hierarchy_level")
    another_informations.teaching_research_activity_text = data.get(
        "teaching_research_activity_text"
    )
    another_informations.tax_withholding = data.get("tax_withholding")
    another_informations.service_shift = data.get("service_shift")
    another_informations.nature_organization = data.get("nature_organization")
    another_informations.attendance = data.get("attendance")
    another_informations.covenant = data.get("covenant")

    db.session.commit()


def get_another_informations(
    fces_id: int, with_commissions_types_and_leavings_list: bool = True
) -> AnotherInformations:

    get_fces(fces_id=fces_id)

    another_informations = (
        AnotherInformations.query.options(
            joinedload("leavings_selected"), joinedload("commission_types_selected")
        )
        .filter(
            AnotherInformations.fces_id == fces_id,
        )
        .first()
    )

    if another_informations is None:
        raise DefaultException("another_informations_not_found", code=404)

    if with_commissions_types_and_leavings_list:
        leavings = get_leavings()
        commission_types = get_commission_types()

        another_informations.leavings = leavings
        another_informations.commission_types = commission_types

    return another_informations


def _verify_unique_data(fces_id: int, sanitary_number: str, filters: list = []):

    if (
        another_informations := AnotherInformations.query.with_entities(
            AnotherInformations.fces_id, AnotherInformations.sanitary_number
        )
        .filter(
            or_(
                AnotherInformations.fces_id == fces_id,
                AnotherInformations.sanitary_number == sanitary_number,
            ),
            *filters,
        )
        .first()
    ):
        if another_informations.fces_id == fces_id:
            raise DefaultException("fces_id_in_use", code=409)
        else:
            raise DefaultException("sanitary_number_in_use", code=409)


from app.main.service.custom_fields import date_from_string
from app.main.service.fces.another_informations.commission_type_service import (
    get_commission_types,
    validate_commission_types,
)
from app.main.service.fces.another_informations.leavings_service import (
    get_leavings,
    validate_leavings,
)
from app.main.service.fces.fces_service import get_fces
