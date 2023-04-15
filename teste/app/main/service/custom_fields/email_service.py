from flask_restx import fields


class Email(fields.String):

    __schema_type__ = "string"
    __schema_format__ = "email"
    __schema_example__ = "string@gmail.com"

    def __init__(self, *args, **kwargs):
        super(Email, self).__init__(*args, **kwargs)
        self.pattern = "([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})"
