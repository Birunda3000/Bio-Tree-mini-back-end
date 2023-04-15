import pytest

@pytest.fixture()
def base_regional_council():
    """Base regional_council data"""

    regional_council = {
        "professional_id": 2,
        "agency_id": 2,
        "regional_council_number": "123456",
        "FU_of_council": "CE",
        "actual": True,
        "last_occurrence_of_SCNES": "24/08/1989",
    }

    return regional_council