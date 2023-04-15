import pytest

from app.main import db
from app.main.service import change_patient_queue, create_default_queues
from app.test.seeders import (
    create_base_seed_patient,
    create_base_seed_professional,
    create_base_seed_queue_manager,
    create_base_seed_risk_classification,
    create_base_seed_vaccine_application,
    create_base_seed_vaccine_application_request,
)


@pytest.fixture(scope="module")
def seeded_database(database):
    """Seed database with vaccines applications"""
    create_default_queues()
    create_base_seed_professional(db)
    create_base_seed_patient(db)
    create_base_seed_queue_manager(db)
    create_base_seed_vaccine_application_request(db)
    create_base_seed_vaccine_application(db)
    create_base_seed_risk_classification(db)


@pytest.mark.usefixtures("seeded_database")
class TestVaccineApplicationApplicationController:

    # --------------------- GET VACCINE APPLICATION HISTORY ---------------------

    def test_get_vaccine_application_with_patient_id_1(self, client):
        response = client.get("/vaccine_application", query_string={"patient_id": 1})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 1
        assert response.json["total_pages"] == 1

        assert response.json["items"][0]["id"] == 1
        assert response.json["items"][0]["professional_id"] == 1
        assert response.json["items"][0]["patient"]["id"] == 1
        assert response.json["items"][0]["vaccine_name"] == "BCG"
        assert response.json["items"][0]["application_type"] == "Aplicação"
        assert (
            response.json["items"][0]["manufacturer"]
            == "F.A.P. - FUNDACAO ATAULPHO DE PAIVA"
        )
        assert response.json["items"][0]["batch"] == "1x4654"
        assert response.json["items"][0]["administration_route"] == "Oral"
        assert response.json["items"][0]["application_site"] == "Rede venosa"
        assert response.json["items"][0]["pregnancy_type"] == "Não se aplica"
        assert response.json["items"][0]["performed_at"] == "07/01/2023"

    def test_get_vaccine_application_with_patient_id_2(self, client):
        response = client.get("/vaccine_application", query_string={"patient_id": 2})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 1
        assert response.json["total_pages"] == 1

        assert response.json["items"][0]["id"] == 2
        assert response.json["items"][0]["professional_id"] == 2
        assert response.json["items"][0]["patient"]["id"] == 2
        assert response.json["items"][0]["vaccine_name"] == "Hepatite B"
        assert response.json["items"][0]["application_type"] == "Resgate"
        assert (
            response.json["items"][0]["manufacturer"]
            == "F.A.P. - FUNDACAO ATAULPHO DE PAIVA"
        )
        assert response.json["items"][0]["batch"] == "1x8795"
        assert response.json["items"][0]["administration_route"] == "Subcutânea"
        assert response.json["items"][0]["application_site"] == "Deltóide direito"
        assert response.json["items"][0]["pregnancy_type"] == "Não se aplica"
        assert response.json["items"][0]["performed_at"] == "25/12/2022"

    def test_get_vaccine_application_by_page(self, client):
        response = client.get("/vaccine_application", query_string={"page": 2})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert len(response.json["items"]) == 0
        assert response.json["current_page"] == 2

    @pytest.mark.parametrize(
        "key, value, total_items",
        [
            ("professional_id", 1, 1),
            ("professional_name", "Profissional teste 1 nome social", 1),
            ("patient_id", 1, 1),
            ("patient_name", "Patient social name 1", 1),
            ("patient_mother_name", "Mãe patient teste 1", 1),
            ("vaccine_name", "BCG", 1),
            ("performed_at", "07/01/2023", 1),
        ],
        ids=[
            "professional_id",
            "professional_name",
            "patient_id",
            "patient_name",
            "patient_mother_name",
            "vaccine_name",
            "performed_at",
        ],
    )
    def test_get_vaccine_application_by(self, client, key, value, total_items):
        response = client.get("/vaccine_application", query_string={key: value})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["total_items"] == total_items

    # --------------------- CREATE VACCINE APPLICATION ---------------------

    @pytest.mark.parametrize(
        "key_popped",
        [
            "professional_id",
            "patient_id",
            "vaccine_name",
            "batch",
            "manufacturer",
            "administration_route",
            "application_site",
            "bottle_type",
            "bottle_doses_number",
            "pregnancy_type",
            "performed_at",
        ],
        ids=[
            "without_professional_id",
            "without_patient_id",
            "without_vaccine_name",
            "without_batch",
            "without_manufacturer",
            "without_administration_route",
            "without_application_site",
            "without_bottle_type",
            "without_bottle_doses_number",
            "without_pregnancy_type",
            "without_performed_at",
        ],
    )
    def test_create_vaccine_application_without_required_data(
        self, client, base_vaccine_application_application, key_popped
    ):
        base_vaccine_application_application.pop(key_popped, None)

        response = client.post(
            "/vaccine_application/application",
            json=base_vaccine_application_application,
        )

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert key_popped in response.json["errors"].keys()

    @pytest.mark.parametrize(
        "key,new_value,expected_message",
        [
            ("patient_id", 0, "patient_not_found"),
            ("professional_id", 0, "professional_not_found"),
            ("request_id", 0, "vaccine_application_request_not_found"),
        ],
        ids=[
            "invalid_patient_id",
            "invalid_professional_id",
            "invalid_request_id",
        ],
    )
    def test_create_vaccine_application_with_invalid_data(
        self,
        client,
        base_vaccine_application_application,
        key,
        new_value,
        expected_message,
    ):
        change_patient_queue({"patient_id": 1, "queue_id": 5})

        base_vaccine_application_application[key] = new_value

        response = client.post(
            "/vaccine_application/application",
            json=base_vaccine_application_application,
        )

        assert response.status_code == 404
        assert response.json["message"] == expected_message

        change_patient_queue({"patient_id": 1, "queue_id": 1})

    @pytest.mark.parametrize(
        "key,new_value",
        [
            ("administration_route", "invalid_administration_route"),
            ("application_site", "invalid_application_site"),
            ("pregnancy_type", "invalid_pregnancy_type"),
        ],
        ids=[
            "invalid_administration_route",
            "invalid_application_site",
            "invalid_pregnancy_type",
        ],
    )
    def test_create_vaccine_application_with_invalid_dto_data(
        self, client, base_vaccine_application_application, key, new_value
    ):
        base_vaccine_application_application[key] = new_value

        response = client.post(
            "/vaccine_application/application",
            json=base_vaccine_application_application,
        )

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert key in response.json["errors"].keys()

    def test_create_vaccine_application_with_patient_not_in_vaccination_queue(
        self, client, base_vaccine_application_application
    ):

        response = client.post(
            "/vaccine_application/application",
            json=base_vaccine_application_application,
        )

        assert response.status_code == 409
        assert response.json["message"] == "patient_not_in_vaccination_queue"

    def test_create_vaccine_application_with_invalid_request(
        self, client, base_vaccine_application_application
    ):
        change_patient_queue({"patient_id": 1, "queue_id": 5})

        base_vaccine_application_application["request_id"] = 2

        response = client.post(
            "/vaccine_application/application",
            json=base_vaccine_application_application,
        )

        assert response.status_code == 409
        assert response.json["message"] == "vaccine_application_request_invalid"

        change_patient_queue({"patient_id": 1, "queue_id": 1})

    def test_create_vaccine_application(
        self, client, base_vaccine_application_application
    ):
        change_patient_queue({"patient_id": 1, "queue_id": 5})

        response = client.post(
            "/vaccine_application/application",
            json=base_vaccine_application_application,
        )

        assert response.status_code == 201
        assert response.json["message"] == "vaccine_application_created"

        change_patient_queue({"patient_id": 1, "queue_id": 1})
