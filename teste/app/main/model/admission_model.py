from sqlalchemy import func

from app.main import db

ADMISSION_TYPES = ["Observação", "Internação"]


class Admission(db.Model):
    __tablename__ = "admission"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"), nullable=False)
    professional_id = db.Column(
        db.Integer, db.ForeignKey("professional.id"), nullable=False
    )
    bed_id = db.Column(db.Integer, db.ForeignKey("bed.id"), nullable=False)
    admitted_at = db.Column(db.DateTime, server_default=func.now())
    type = db.Column(db.Enum(*ADMISSION_TYPES, name="admission_type"), nullable=False)

    patient = db.relationship("Patient", back_populates="admission")
    professional = db.relationship("Professional", back_populates="admission")
    bed = db.relationship("Bed", back_populates="admission")
    vital_signs_controls = db.relationship(
        "VitalSignsControl", back_populates="admission"
    )
    actions = db.relationship("AdmissionActionAssociation", back_populates="admission")
    questions = db.relationship(
        "AdmissionQuestionAssociation", back_populates="admission"
    )
    histories = db.relationship("History", back_populates="admission")

    def __repr__(self) -> str:
        return f"<Admission {self.id}>"
