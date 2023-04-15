from sqlalchemy.orm.exc import NoResultFound

from app.main.exceptions import DefaultException
from app.main.model import VitalSignsControl


def get_vital_signs_control(
    vital_signs_control_id: int, options: list = None
) -> VitalSignsControl:

    query = VitalSignsControl.query

    if options is not None:
        query = query.options(*options)

    vital_signs_control = query.get(vital_signs_control_id)

    if vital_signs_control is None:
        raise DefaultException("vital_signs_control_not_found", code=404)

    return vital_signs_control
