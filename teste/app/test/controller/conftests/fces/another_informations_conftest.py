import pytest


@pytest.fixture()
def base_another_informations():
    """Base another informations data"""

    another_informations = {
        "sanitary_number": "654987",
        "issuance_date": "11/02/1976",
        "issuing_agency": "SES",
        "bank": "001",
        "agency": "string",
        "current_account": "string",
        "administrative_field": "Federal",
        "hierarchy_level": "string",
        "teaching_research_activity_text": "string",
        "tax_withholding": "IRPJ",
        "service_shift": "Manhã",
        "nature_organization": "Administração Direta da Saúde",
        "attendance": "string",
        "covenant": "Público",
        "leavings_selected": [1, 2],
        "commission_types_selected": [2, 5, 9],
    }

    return another_informations
