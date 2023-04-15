from flask_restx import fields

from app.main import cpf_validator


class CPF(fields.String):

    __schema_type__ = "string"
    __schema_format__ = "cpf"
    __schema_example__ = cpf_validator.generate()

    def __init__(self, *args, **kwargs):
        super(CPF, self).__init__(*args, **kwargs)
        self.min_length = 11
        self.max_length = 11

    def parse(self, value):
        if value is None:
            return None
        try:
            if isinstance(value, str):
                cpf_validator.validate(value)
                return value
        except ValueError as e:
            raise ValueError("Unsupported CPF format") from e

    def format(self, value):
        try:
            return self.parse(value)
        except ValueError as e:
            raise fields.MarshallingError(e)
