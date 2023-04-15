from flask_restx import fields


class Phone(fields.String):

    __schema_type__ = "string"
    __schema_format__ = "phone"
    __schema_example__ = "8532165498"

    def __init__(self, *args, **kwargs):
        super(Phone, self).__init__(*args, **kwargs)
        self.min_length = 10
        self.max_length = 10
