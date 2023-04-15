import random
import time as timex
from datetime import datetime, time

random.seed(timex.time())

from flask_restx import fields


def time_from_string(value: str):
    if value is None:
        return None
    return time.strptime(value, "%H:%M:%S")


def time_to_string(value: time):
    if value is None:
        return None
    return value.strftime("%H:%M:%S")


class CustomTime(fields.Raw):

    __schema_type__ = "string"
    __schema_format__ = "custom_time"
    __schema_example__ = "{:02d}:{:02d}:{:02d}".format(
        random.randint(0, 23),
        random.randint(0, 59),
        random.randint(0, 59),
    )

    def __init__(self, **kwargs):
        super(CustomTime, self).__init__(**kwargs)

    def parse(self, value):
        if value is None:
            return None
        try:
            if isinstance(value, str):
                return time_from_string(value)
            elif isinstance(value, time):
                return value
            elif isinstance(value, datetime):
                return time(value.hour, value.minute, value.second)
        except ValueError as e:
            raise ValueError("Unsupported CustomTime format") from e

    def format(self, value):
        try:
            value = self.parse(value)
            return time_to_string(value)
        except ValueError as e:
            raise fields.MarshallingError(e)
