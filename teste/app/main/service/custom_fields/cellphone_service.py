from flask_restx import fields


class CellPhone(fields.String):

    __schema_type__ = "string"
    __schema_format__ = "cellphone"
    __schema_example__ = "85987654321"

    def __init__(self, *args, **kwargs):
        super(CellPhone, self).__init__(*args, **kwargs)
        self.min_length = 11
        self.max_length = 11
