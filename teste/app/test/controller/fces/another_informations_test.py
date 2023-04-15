import pytest
from sqlalchemy.orm import joinedload

from app.main import db
from app.main.model import AnotherInformations, CommissionType, Leavings
from app.main.service import date_from_string
from app.test.seeders import (
    create_base_seed_another_informations,
    create_base_seed_commission_type,
    create_base_seed_fces,
    create_base_seed_leavings,
    create_base_seed_maintainer,
    create_base_seed_professional,
    create_base_seed_sanitary_district,
)


@pytest.fixture(scope="module")
def seeded_database(client, database):
    """Seed database with another informations data"""
    create_base_seed_professional(db)
    create_base_seed_maintainer(db)
    create_base_seed_sanitary_district(db)
    create_base_seed_fces(db)
    create_base_seed_commission_type(db)
    create_base_seed_leavings(db)

    return create_base_seed_another_informations(db)


@pytest.mark.usefixtures("seeded_database")
class TestAnotherInformations:
    # --------------------- GET  ---------------------

    def test_get_another_informations(self, client):
        response = client.get("/fces/1/another_informations")

        assert response.status_code == 200
        assert len(response.json) == 19
        assert response.json["id"] == 1
        assert response.json["sanitary_number"] == "54321"
        assert response.json["issuance_date"] == "29/09/2020"
        assert response.json["issuing_agency"] == "SES"
        assert response.json["bank"] == "249"
        assert response.json["agency"] == "6491"
        assert response.json["current_account"] == "619949"
        assert response.json["administrative_field"] == "Federal"
        assert response.json["hierarchy_level"] == "Nível de hierarquia"
        assert (
            response.json["teaching_research_activity_text"] == "Hospital Universitário"
        )
        assert response.json["tax_withholding"] == "IRPJ"
        assert response.json["service_shift"] == "Noite"
        assert response.json["nature_organization"] == "Empresa"
        assert response.json["attendance"] == "Atendimento"
        assert response.json["covenant"] == "Público"
        assert response.json["leavings_selected"][0]["id"] == 1
        assert response.json["commission_types_selected"][0]["id"] == 1

    def test_get_another_informations_by_invalid_fces_id(self, client):
        response = client.get("/fces/0/another_informations")

        assert response.status_code == 404
        assert response.json["message"] == "fces_not_found"

    # --------------------- UPDATE ---------------------

    @pytest.mark.parametrize(
        "key",
        [
            "issuing_agency",
            "tax_withholding",
            "service_shift",
            "nature_organization",
            "covenant",
        ],
        ids=[
            "register_with_wrong_issuing_agency",
            "register_with_wrong_tax_withholding",
            "register_with_wrong_service_shift",
            "register_with_wrong_nature_organization",
            "register_with_wrong_covenant",
        ],
    )
    def test_update_another_informations_with_wrong_enum_data(
        self, client, base_another_informations, key
    ):
        base_another_informations[key] = "teste"
        response = client.put(
            "/fces/1/another_informations", json=base_another_informations
        )

        assert response.json["message"] == "Input payload validation failed"
        assert response.status_code == 400
        assert key in response.json["errors"].keys()

    @pytest.mark.parametrize(
        "required_data",
        [
            "sanitary_number",
            "issuance_date",
            "issuing_agency",
            "bank",
            "agency",
            "current_account",
            "administrative_field",
            "hierarchy_level",
            "tax_withholding",
            "service_shift",
            "nature_organization",
            "attendance",
            "covenant",
        ],
    )
    def test_update_another_informations_without_required_data(
        self, client, base_another_informations, required_data
    ):
        del base_another_informations[required_data]

        response = client.put(
            "fces/1/another_informations", json=base_another_informations
        )

        assert response.json["message"] == "Input payload validation failed"
        assert response.status_code == 400

    def test_update_another_informations_without_minimal_length_data(
        self, client, base_another_informations
    ):
        base_another_informations["leavings_selected"] = []

        response = client.put(
            "fces/1/another_informations", json=base_another_informations
        )

        assert response.json["message"] == "Input payload validation failed"
        assert response.status_code == 400

    def test_update_another_informations_with_registered_data(
        self, client, base_another_informations
    ):
        base_another_informations["sanitary_number"] = "12345"
        response = client.put(
            "fces/1/another_informations", json=base_another_informations
        )

        assert response.json["message"] == "sanitary_number_in_use"
        assert response.status_code == 409

    def test_update_another_informations_invalid_fces_id(
        self, client, base_another_informations
    ):
        response = client.put(
            "fces/0/another_informations", json=base_another_informations
        )

        assert response.json["message"] == "fces_not_found"
        assert response.status_code == 404

    @pytest.mark.parametrize(
        "key,expected_message",
        [
            ("commission_types_selected", "commission_type_not_found"),
            ("leavings_selected", "leavings_not_found"),
        ],
    )
    def test_update_another_informations_with_invalid_data(
        self, client, base_another_informations, key, expected_message
    ):
        base_another_informations[key] = [0]
        response = client.put(
            "fces/1/another_informations", json=base_another_informations
        )

        assert response.json["message"] == expected_message
        assert response.status_code == 404

    def test_update_invalid_another_informations(
        self, client, base_another_informations
    ):
        response = client.put(
            "fces/3/another_informations", json=base_another_informations
        )

        assert response.json["message"] == "another_informations_not_found"
        assert response.status_code == 404

    def test_update_another_informations(self, client, base_another_informations):
        response = client.put(
            "fces/1/another_informations", json=base_another_informations
        )

        assert response.json["message"] == "another_informations_updated"
        assert response.status_code == 200

        another_informations = (
            AnotherInformations.query.options(
                joinedload("commission_types_selected"), joinedload("leavings_selected")
            )
            .filter_by(id=1)
            .first()
        )
        commission_types = CommissionType.query.filter(
            CommissionType.id.in_({2, 5, 9})
        ).all()
        leavings = Leavings.query.filter(Leavings.id.in_({1, 2})).all()

        assert another_informations.sanitary_number == "654987"
        assert another_informations.issuance_date == date_from_string("11/02/1976")
        assert another_informations.bank == "001"
        assert another_informations.agency == "string"
        assert another_informations.current_account == "string"
        assert another_informations.hierarchy_level == "string"
        assert another_informations.teaching_research_activity_text == "string"
        assert another_informations.service_shift == "Manhã"
        assert (
            another_informations.nature_organization == "Administração Direta da Saúde"
        )
        assert another_informations.attendance == "string"
        assert another_informations.commission_types_selected == commission_types
        assert another_informations.leavings_selected == leavings

        self._undo_another_informations_update_changes()

    # --------------------- CREATE ---------------------

    @pytest.mark.parametrize(
        "key",
        [
            "issuing_agency",
            "tax_withholding",
            "service_shift",
            "nature_organization",
            "covenant",
        ],
        ids=[
            "register_with_wrong_issuing_agency",
            "register_with_wrong_tax_withholding",
            "register_with_wrong_service_shift",
            "register_with_wrong_nature_organization",
            "register_with_wrong_covenant",
        ],
    )
    def test_create_another_informations_with_wrong_enum_data(
        self, client, base_another_informations, key
    ):
        base_another_informations[key] = "teste"
        response = client.post(
            "/fces/1/another_informations", json=base_another_informations
        )

        assert response.json["message"] == "Input payload validation failed"
        assert response.status_code == 400
        assert key in response.json["errors"].keys()

    @pytest.mark.parametrize(
        "required_data",
        [
            "sanitary_number",
            "issuance_date",
            "issuing_agency",
            "bank",
            "agency",
            "current_account",
            "administrative_field",
            "hierarchy_level",
            "tax_withholding",
            "service_shift",
            "nature_organization",
            "attendance",
            "covenant",
        ],
    )
    def test_create_another_informations_without_required_data(
        self, client, base_another_informations, required_data
    ):
        del base_another_informations[required_data]

        response = client.post(
            "fces/1/another_informations", json=base_another_informations
        )

        assert response.json["message"] == "Input payload validation failed"
        assert response.status_code == 400

    def test_create_another_informations_alredy_created(
        self, client, base_another_informations
    ):

        response = client.post(
            "fces/1/another_informations", json=base_another_informations
        )

        assert response.json["message"] == "fces_id_in_use"
        assert response.status_code == 409

    def test_create_another_informations_with_registered_data(
        self, client, base_another_informations
    ):
        base_another_informations["sanitary_number"] = "12345"
        response = client.post(
            "fces/3/another_informations", json=base_another_informations
        )

        assert response.json["message"] == "sanitary_number_in_use"
        assert response.status_code == 409

    @pytest.mark.parametrize(
        "key",
        [
            ("commission_types_selected", "commission_type"),
            ("leavings_selected", "leavings"),
        ],
    )
    def test_create_another_informations_with_invalid_data(
        self, client, base_another_informations, key
    ):
        base_another_informations[key[0]] = [0]
        response = client.post(
            "fces/3/another_informations", json=base_another_informations
        )

        assert response.json["message"] == f"{key[1]}_not_found"
        assert response.status_code == 404

    def test_create_another_informations_invalid_fces_id(
        self, client, base_another_informations
    ):
        response = client.post(
            "fces/0/another_informations", json=base_another_informations
        )

        assert response.json["message"] == "fces_not_found"
        assert response.status_code == 404

    def test_create_another_informations(self, client, base_another_informations):
        response = client.post(
            "fces/3/another_informations", json=base_another_informations
        )

        assert response.json["message"] == "another_informations_created"
        assert response.status_code == 201

    # --------------------- Helper functions  ---------------------

    def _undo_another_informations_update_changes(self) -> None:
        another_informations = AnotherInformations.query.get(1)

        another_informations.sanitary_number = "54321"

        db.session.commit()
