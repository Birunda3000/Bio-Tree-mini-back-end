from sqlalchemy import and_, or_

from app.main.model import Patient, Professional


def patient_name_filter(patient_name: str):
    return or_(
        and_(
            Patient.social_name != None,
            Patient.social_name.ilike(f"%{patient_name}%"),
        ),
        and_(
            Patient.social_name == None,
            Patient.name.ilike(f"%{patient_name}%"),
        ),
    )


def professional_name_filter(professional_name: str):
    return or_(
        and_(
            Professional.social_name != None,
            Professional.social_name.ilike(f"%{professional_name}%"),
        ),
        and_(
            Professional.social_name == None,
            Professional.name.ilike(f"%{professional_name}%"),
        ),
    )
