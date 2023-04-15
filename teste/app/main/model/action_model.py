from sqlalchemy.orm import validates

from app.main import db
from app.main.model.prescription_action_table import prescription_action


class Action(db.Model):
    __tablename__ = "action"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    prescriptions = db.relationship(
        "Prescription",
        secondary=prescription_action,
        back_populates="actions",
    )
    admission = db.relationship("AdmissionActionAssociation", back_populates="actions")
    history = db.relationship(
        "HistoryNursingPrescriptionAction", back_populates="action"
    )

    def __repr__(self):
        return f"<Action {self.name}>"

    @validates("name")
    def convert_upper(self, key, value):
        return value.upper()
