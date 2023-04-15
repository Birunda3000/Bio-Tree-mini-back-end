import random
import time as timex
from datetime import date, datetime

random.seed(timex.time())

from flask_restx import fields


def date_from_string(value: str):
    if value is None:
        return None
    return datetime.strptime(value, "%d/%m/%Y").date()


def date_to_string(value: date):
    if value is None:
        return None
    return value.strftime("%d/%m/%Y")


class CustomDate(fields.Date):
    __schema_format__ = "custom_date"
    __schema_example__ = "{:02d}/{:02d}/{:04d}".format(
        random.randint(1, 28),
        random.randint(1, 12),
        random.randint(1970, datetime.now().year),
    )

    def parse(self, value):
        if value is None:
            return None
        try:
            if isinstance(value, str):
                return date_from_string(value)
            elif isinstance(value, datetime):
                return value.date()
            elif isinstance(value, date):
                return value
        except ValueError as e:
            raise ValueError("Unsupported CustomDate format") from e

    def format(self, value):
        try:
            value = self.parse(value)
            return date_to_string(value)
        except ValueError as e:
            raise fields.MarshallingError(e)


class CustomDateFuture(CustomDate):
    __schema_format__ = "custom_date_future"
    __schema_example__ = "{:02d}/{:02d}/{:04d}".format(
        random.randint(1, 28),
        random.randint(1, 12),
        random.randint(datetime.now().year, datetime.now().year + 100),
    )


class CustomDatePast(CustomDate):
    __schema_format__ = "custom_date_past"
    __schema_example__ = "{:02d}/{:02d}/{:04d}".format(
        random.randint(1, 28),
        random.randint(1, 12),
        random.randint(1970, datetime.now().year),
    )
