from app.main import db


class AdmissionActionAssociation(db.Model):
    __tablename__ = "admission_action_association"

    admission_id = db.Column(
        db.Integer, db.ForeignKey("admission.id"), nullable=False, primary_key=True
    )
    action_id = db.Column(
        db.Integer, db.ForeignKey("action.id"), nullable=False, primary_key=True
    )
    recurrence = db.Column(db.String, nullable=False)

    admission = db.relationship("Admission", back_populates="actions")
    actions = db.relationship("Action", back_populates="admission")

    def __repr__(self) -> str:
        return f"<AdmissionActionAssociation {self.admission_id}>"
