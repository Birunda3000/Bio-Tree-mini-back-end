import io
import os

import pytest

from app.main import db
from app.main.model import Procedure
from app.main.service import activate_procedure, inactivate_procedure
from app.test.seeders import create_base_seed_procedure

PROCEDURES_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    "resources",
    "procedures",
)


@pytest.fixture(scope="module")
def seeded_database(database):
    """Seed database with procedure data"""
    return create_base_seed_procedure(db)


@pytest.fixture()
def post_procedures_with_file(client):
    """Return response of post request with file"""

    def _post_procedures_with_file(file_name: str):
        file_path = os.path.join(PROCEDURES_DIR, file_name)

        with open(file_path, "rb") as file:
            response = client.post("/procedure", data={"file": (file, file_name)})
        return response

    return _post_procedures_with_file


class TestProcedureController:

    # --------------------- GET PROCEDURES ---------------------

    def test_get_procedures(self, client, seeded_database):
        response = client.get("/procedure")

        assert response.status_code == 200
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 3
        assert response.json["total_pages"] == 1

        first_item = response.json["items"][0]

        assert len(first_item) == 7
        assert first_item["code"] == "9965"
        assert first_item["classification"] == "06.04.36.004"
        assert first_item["description"] == "ATORVASTATINA 80 MG (POR COMPRIMIDO)"

    def test_get_procedures_by_page(self, client, seeded_database):
        response = client.get("/procedure", query_string={"page": 2})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 2
        assert len(response.json["items"]) == 0

    def test_get_procedure_and_show_inactivated(self, client, seeded_database):
        inactivate_procedure(1)

        response = client.get("/procedure", query_string={"show_inactivated": True})

        assert response.status_code == 200
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 3

        first_item = response.json["items"][0]

        assert len(first_item) == 7
        assert first_item["code"] == "9965"
        assert first_item["active"] == False

        activate_procedure(1)

    @pytest.mark.parametrize(
        "description,total_items",
        [("ATORVASTATINA 80 MG (POR COMPRIMIDO)", 1), ("COMPRIMIDO", 2)],
        ids=["complete_description", "incomplete_description"],
    )
    def test_get_procedure_by_description(
        self, client, seeded_database, description, total_items
    ):
        response = client.get("/procedure", query_string={"description": description})

        assert response.status_code == 200
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == total_items

        first_item = response.json["items"][0]

        assert len(first_item) == 7
        assert first_item["code"] == "9965"

    @pytest.mark.parametrize(
        "classification,total_items",
        [("06.04.36.004", 1), ("06.04.", 2)],
        ids=["complete_classification", "incomplete_classification"],
    )
    def test_get_procedure_by_classification(
        self, client, seeded_database, classification, total_items
    ):
        response = client.get(
            "/procedure", query_string={"classification": classification}
        )

        assert response.status_code == 200
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == total_items

        first_item = response.json["items"][0]

        assert len(first_item) == 7
        assert first_item["code"] == "9965"

    # --------------------- INACTIVATE PROCEDURES ---------------------

    def test_inactivate_non_registered_procedure(self, client, seeded_database):
        response = client.patch("/procedure/inactivate/0")

        assert response.status_code == 404
        assert response.json["message"] == "procedure_not_found"

    def test_inactivate_already_inactive_procedure(self, client, seeded_database):
        inactivate_procedure(1)

        response = client.patch("/procedure/inactivate/1")

        assert response.status_code == 409
        assert response.json["message"] == "procedure_is_inactive"

        activate_procedure(1)

    def test_inactivate_procedure(self, client, seeded_database):
        response = client.patch("/procedure/inactivate/1")

        assert response.status_code == 200
        assert response.json["message"] == "procedure_inactivated"

        procedure = Procedure.query.get(1)
        assert procedure.active == False

        activate_procedure(1)

    # --------------------- ACTIVATE PROCEDURES ---------------------

    def test_activate_non_registered_procedure(self, client, seeded_database):
        response = client.patch("/procedure/activate/0")

        assert response.status_code == 404
        assert response.json["message"] == "procedure_not_found"

    def test_activate_already_active_procedure(self, client, seeded_database):
        response = client.patch("/procedure/activate/1")

        assert response.status_code == 409
        assert response.json["message"] == "procedure_is_active"

    def test_activate_procedure(self, client, seeded_database):
        inactivate_procedure(1)

        response = client.patch("/procedure/activate/1")

        assert response.status_code == 200
        assert response.json["message"] == "procedure_activated"

        procedure = Procedure.query.get(1)
        assert procedure.active == True

    # --------------------- UPLOAD PROCEDURES ---------------------

    def test_upload_procedures_with_diffent_number_of_columns(
        self, database, post_procedures_with_file
    ):
        response = post_procedures_with_file(file_name="procedures_missing_column.pdf")

        assert response.status_code == 400
        assert response.json["message"] == "invalid_columns_file"
        assert "file" in response.json["errors"].keys()

    def test_upload_procedures_with_existing_data(
        self, seeded_database, post_procedures_with_file
    ):
        response = post_procedures_with_file(
            file_name="procedures_added_with_different_values.pdf"
        )

        assert response.status_code == 201
        assert response.json["message"] == "procedures_uploaded"

        procedures = Procedure.query.all()

        # Check if saved values are updated based on pdf
        assert len(procedures) == 3
        assert procedures[0].code == "9965"
        assert procedures[0].price == 10.00
        assert procedures[1].code == "9911"
        assert procedures[1].dv == 2

    def test_upload_procedures_with_non_pdf_file(self, client, database):
        response = client.post(
            "/procedure", data={"file": (io.BytesIO(), "invalid_file.png")}
        )

        assert response.status_code == 400
        assert response.json["message"] == "invalid_type_file"
        assert "file" in response.json["errors"].keys()

    def test_upload_procedures(self, database, post_procedures_with_file):
        response = post_procedures_with_file(file_name="procedures_complete.pdf")

        assert response.status_code == 201
        assert response.json["message"] == "procedures_uploaded"

        procedures = Procedure.query.all()

        assert len(procedures) == 4
        assert procedures[0].code == "9965"
        assert procedures[0].classification == "06.04.36.004"
        assert procedures[0].description == "ATORVASTATINA 80 MG (POR COMPRIMIDO)"
        assert procedures[0].price == 0.00
        assert procedures[0].active == True
