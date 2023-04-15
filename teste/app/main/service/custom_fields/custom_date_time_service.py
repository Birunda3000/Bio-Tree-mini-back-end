import random
import time as timex
from datetime import date, datetime

random.seed(timex.time())

from flask_restx import fields


def datetime_from_string(value: str):
    if value is None:
        return None
    return datetime.strptime(value, "%d/%m/%Y %H:%M:%S")


def datetime_to_string(value: datetime):
    if value is None:
        return None
    return value.strftime("%d/%m/%Y %H:%M:%S")


class CustomDateTime(fields.DateTime):
    __schema_format__ = "custom_datetime"
    __schema_example__ = "{:02d}/{:02d}/{:04d} {:02d}:{:02d}:{:02d}".format(
        random.randint(1, 28),
        random.randint(1, 12),
        random.randint(1970, datetime.now().year),
        random.randint(0, 23),
        random.randint(0, 59),
        random.randint(0, 59),
    )

    def parse(self, value):
        if value is None:
            return None
        try:
            if isinstance(value, str):
                return datetime_from_string(value)
            elif isinstance(value, datetime):
                return value
            elif isinstance(value, date):
                return datetime(value.year, value.month, value.day)
        except ValueError as e:
            raise ValueError("Unsupported CustomDateTime format") from e

    def format(self, value):
        try:
            value = self.parse(value)
            return datetime_to_string(value)
        except ValueError as e:
            raise fields.MarshallingError(e)


class CustomDateTimeFuture(CustomDateTime):
    __schema_format__ = "custom_datetime_future"
    __schema_example__ = "{:02d}/{:02d}/{:04d} {:02d}:{:02d}:{:02d}".format(
        random.randint(1, 28),
        random.randint(1, 12),
        random.randint(datetime.now().year, datetime.now().year + 100),
        random.randint(0, 23),
        random.randint(0, 59),
        random.randint(0, 59),
    )


class CustomDateTimePast(CustomDateTime):
    __schema_format__ = "custom_datetime_past"
    __schema_example__ = "{:02d}/{:02d}/{:04d} {:02d}:{:02d}:{:02d}".format(
        random.randint(1, 28),
        random.randint(1, 12),
        random.randint(1970, datetime.now().year),
        random.randint(0, 23),
        random.randint(0, 59),
        random.randint(0, 59),
    )
