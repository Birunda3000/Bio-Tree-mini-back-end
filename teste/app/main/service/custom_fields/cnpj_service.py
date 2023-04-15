from flask_restx import fields

from app.main import cnpj_validator


class CNPJ(fields.String):

    __schema_type__ = "string"
    __schema_format__ = "cnpj"
    __schema_example__ = cnpj_validator.generate()

    def __init__(self, *args, **kwargs):
        super(CNPJ, self).__init__(*args, **kwargs)
        self.min_length = 14
        self.max_length = 14

    def parse(self, value):
        if value is None:
            return None
        try:
            if isinstance(value, str):
                cnpj_validator.validate(value)
                return value
        except ValueError as e:
            raise ValueError("Unsupported CNPJ format") from e

    def format(self, value):
        try:
            return self.parse(value)
        except ValueError as e:
            raise fields.MarshallingError(e)
