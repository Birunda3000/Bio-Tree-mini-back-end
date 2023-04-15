from ..enum import STATES_OPTIONS
from app.main import db
from .professional_model import *

class Address(db.Model):
    __tablename__ = "address"

    id = db.Column(db.Integer, primary_key=True)
    cep = db.Column(db.String(8), nullable=False)
    state = db.Column(db.Enum(*STATES_OPTIONS, name="state_enum"), nullable=False)# address_UF
    #LOGRADOURO??
    district = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    number = db.Column(db.String, nullable=False)
    complement = db.Column(db.String, nullable=False)

    street = db.Column(db.String, nullable=False)

    professional = db.relationship(
        "Professional", back_populates="address", uselist=False
    )
    patient = db.relationship("Patient", back_populates="address", uselist=False)
    maintainer = db.relationship("Maintainer", back_populates="address", uselist=False)

    def __repr__(self) -> str:
        return f"<Address {self.cep}>"
