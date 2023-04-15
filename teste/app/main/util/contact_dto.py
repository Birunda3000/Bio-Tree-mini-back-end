from flask_restx import Namespace, fields

from app.main.service import CellPhone, Phone


class ContactDTO:
    api = Namespace("contact", description="contact related operations")

    contact = api.model(
        "contact",
        {
            "phone": Phone(description="contact phone"),
            "cellphone": CellPhone(description="contact cellphone"),
            "emergency_contact": CellPhone(description="contact emergency contact"),
            "fax": fields.String(description="contact fax"),
        },
    )
