from app.main.model.regional_council_model import RegionalCouncil
from app.main.model.agency_model import Agency
from app.main.model.professional_model import Professional
from app.main.service import date_from_string
from app.main.service import create_default_agencies_and_occupations

def create_base_seed_regional_council(db):
    """Add 2 RegionalCouncils"""
    create_default_agencies_and_occupations(r'C:\Users\esdn6\Documents\code-hub\back-end\seeders\resources\occupations.txt')
    professional = Professional.query.get(1)
    agency = Agency.query.get(1)
    new_regional_council = RegionalCouncil(
        professional=professional,
        agency=agency,
        regional_council_number="123456",
        FU_of_council="CE",
        actual=True,
        last_occurrence_of_SCNES=date_from_string("24/08/1989"),
    )
    db.session.add(new_regional_council)
    db.session.commit()


