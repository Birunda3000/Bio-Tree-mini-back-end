import io
import os

import pytest

from app.main import db
from app.main.model import Classification, Service
from app.test.seeders import create_base_seed_classification, create_base_seed_service

SERVICE_AND_CLASSIFICATIONS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))),
    "resources",
    "service_classification",
)


@pytest.fixture(scope="module")
def seeded_database(database):
    """Seed database with prescription data"""

    create_base_seed_service(db)
    create_base_seed_classification(db)


@pytest.fixture()
def post_services_and_classifications_with_file(client):
    """Return response of post request with file"""

    def _post_services_and_classifications_with_file(file_name: str):
        file_path = os.path.join(SERVICE_AND_CLASSIFICATIONS_DIR, file_name)

        with open(file_path, "rb") as file:
            response = client.post(
                "/service/classification/upload", data={"file": (file, file_name)}
            )
        return response

    return _post_services_and_classifications_with_file


@pytest.mark.usefixtures("seeded_database")
class TestClassificationController:

    # --------------------- GET ---------------------

    def test_get_classifications(self, client):
        response = client.get("/service/classification")

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 2
        assert response.json["total_pages"] == 1

        assert response.json["items"][0]["id"] == 1
        assert response.json["items"][0]["service_id"] == 1
        assert response.json["items"][0]["name"] == "CLASSIFICATION ONE"
        assert response.json["items"][1]["id"] == 2
        assert response.json["items"][1]["service_id"] == 1
        assert response.json["items"][1]["name"] == "CLASSIFICATION TWO"

    def test_get_classifications_by_name(self, client):
        response = client.get("/service/classification", query_string={"name": "one"})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 1
        assert response.json["total_pages"] == 1

        assert response.json["items"][0]["id"] == 1
        assert response.json["items"][0]["service_id"] == 1
        assert response.json["items"][0]["name"] == "CLASSIFICATION ONE"

    # --------------------- GET BY ID  ---------------------

    def test_get_classification(self, client):
        response = client.get("/service/classification/1")

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["id"] == 1
        assert response.json["code"] == "001"
        assert response.json["service_id"] == 1
        assert response.json["name"] == "CLASSIFICATION ONE"

    def test_get_classification_that_not_exists(self, client):
        response = client.get("/service/classification/0")

        assert response.status_code == 404
        assert response.json["message"] == "classification_not_found"

    # --------------------- UPDATE ---------------------

    @pytest.mark.parametrize(
        "key_popped",
        [
            "service_id",
            "code",
            "name",
        ],
        ids=[
            "update_without_service_id",
            "update_without_code",
            "update_without_name",
        ],
    )
    def test_update_classification_without_required_data(
        self, client, base_classification, key_popped
    ):
        base_classification.pop(key_popped, None)
        response = client.put("/service/classification/2", json=base_classification)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert key_popped in response.json["errors"].keys()

    def test_update_classification_with_invalid_name(self, client, base_classification):
        base_classification["name"] = 0
        response = client.put("/service/classification/1", json=base_classification)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"

    def test_update_classification_with_invalid_code(self, client, base_classification):
        base_classification["code"] = "ABC"
        response = client.put("/service/classification/1", json=base_classification)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"

    def test_update_classification_that_not_exists(self, client, base_classification):
        response = client.put("/service/classification/0", json=base_classification)

        assert response.status_code == 404
        assert response.json["message"] == "classification_not_found"

    def test_update_classification_with_service_id_that_not_exists(
        self, client, base_classification
    ):
        base_classification["service_id"] = 0
        response = client.put("/service/classification/1", json=base_classification)

        assert response.status_code == 404
        assert response.json["message"] == "service_not_found"

    def test_update_classification_with_registered_pair_service_id_and_name(
        self, client, base_classification
    ):
        base_classification["service_id"] = 1
        base_classification["name"] = "CLASSIFICATION TWO"
        response = client.put("/service/classification/1", json=base_classification)

        assert response.status_code == 409
        assert response.json["message"] == "name_in_use"

    def test_update_classification_with_registered_pair_service_id_and_code(
        self, client, base_classification
    ):
        base_classification["service_id"] = 1
        base_classification["code"] = "002"
        response = client.put("/service/classification/1", json=base_classification)

        assert response.status_code == 409
        assert response.json["message"] == "code_in_use"

    def test_update_classification(self, client, base_classification):
        response = client.put("/service/classification/1", json=base_classification)

        assert response.status_code == 200
        assert response.json["message"] == "classification_updated"

        self._undo_classification_update_changes()

    @pytest.mark.parametrize(
        "key, value",
        [
            ("code", "002"),
            ("name", "CLASSIFICATION TWO"),
        ],
        ids=[
            "registered_code",
            "registered_name",
        ],
    )
    def test_update_classification_with_diff_service_and_registered_properties(
        self, client, base_classification, key, value
    ):
        base_classification["service_id"] = 2
        base_classification[key] = value
        response = client.put("/service/classification/1", json=base_classification)

        assert response.status_code == 200
        assert response.json["message"] == "classification_updated"

        self._undo_classification_update_changes()

    # --------------------- POST ---------------------

    @pytest.mark.parametrize(
        "key_popped",
        [
            "service_id",
            "code",
            "name",
        ],
        ids=[
            "create_without_service_id",
            "create_without_code",
            "create_without_name",
        ],
    )
    def test_create_classification_without_required_data(
        self, client, base_classification, key_popped
    ):
        base_classification.pop(key_popped, None)
        response = client.post("/service/classification", json=base_classification)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert key_popped in response.json["errors"].keys()

    @pytest.mark.parametrize(
        "key, value",
        [
            ("name", 0),
            ("code", "ABC"),
        ],
        ids=["invalid_name", "invalid_code"],
    )
    def test_create_classification_with_invalid_properties(
        self, client, base_classification, key, value
    ):
        base_classification[key] = value
        response = client.post("/service/classification", json=base_classification)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert key in response.json["errors"].keys()

    def test_create_classification_with_registered_name(
        self, client, base_classification
    ):
        base_classification["name"] = "CLASSIFICATION ONE"
        response = client.post("/service/classification", json=base_classification)

        assert response.status_code == 409
        assert response.json["message"] == "name_in_use"

    def test_create_classification_with_service_id_that_not_exists(
        self, client, base_classification
    ):
        base_classification["service_id"] = 0
        response = client.post("/service/classification", json=base_classification)

        assert response.status_code == 404
        assert response.json["message"] == "service_not_found"

    @pytest.mark.parametrize(
        "key, value",
        [
            ("code", "002"),
            ("name", "CLASSIFICATION TWO"),
        ],
        ids=[
            "registered_code",
            "registered_name",
        ],
    )
    def test_create_classification_with_registered_pair_service_id_and_properties(
        self, client, base_classification, key, value
    ):
        base_classification["service_id"] = 1
        base_classification[key] = value
        response = client.post("/service/classification", json=base_classification)

        assert response.status_code == 409
        assert response.json["message"] == f"{key}_in_use"

    def test_create_classification(self, client, base_classification):
        response = client.post("/service/classification", json=base_classification)

        assert response.status_code == 201
        assert response.json["message"] == "classification_created"

        self._delete_classifications_from_db(ids=[3])

    @pytest.mark.parametrize(
        "key, value",
        [
            ("code", "002"),
            ("name", "CLASSIFICATION TWO"),
        ],
        ids=[
            "registered_code",
            "registered_name",
        ],
    )
    def test_create_classification_with_diff_service_id_and_registered_properties(
        self, client, base_classification, key, value
    ):
        base_classification["service_id"] = 2
        base_classification[key] = value
        response = client.post("/service/classification", json=base_classification)

        assert response.status_code == 201
        assert response.json["message"] == "classification_created"

        self._delete_classifications_from_db(ids=[3])

    # --------------------- UPLOAD SERVICES AND CLASSIFICATIONS ---------------------

    def test_upload_service_classification_with_non_stardard_file(
        self, post_services_and_classifications_with_file
    ):
        response = post_services_and_classifications_with_file(
            file_name="service_classification_failed.xlsx"
        )
        assert response.status_code == 400
        assert response.json["message"] == "non_standard_file"

    def test_upload_service_classification_with_non_xlsx_or_ods_file(self, client):
        response = client.post(
            "/service/classification/upload",
            data={"file": (io.BytesIO(), "invalid_file.png")},
        )

        assert response.status_code == 400
        assert response.json["message"] == "invalid_type_file"
        assert "file" in response.json["errors"].keys()

    def test_upload_services_and_classifications_from_ods_file(
        self, post_services_and_classifications_with_file
    ):
        response = post_services_and_classifications_with_file(
            file_name="service_classification.ods"
        )

        assert response.json["message"] == "services_and_classifications_uploaded"
        assert response.status_code == 201

        services = Service.query.all()
        classifications = Classification.query.all()

        assert len(services) == 4
        assert services[2].id == 3
        assert services[2].code == "100"
        assert services[2].name == "SERVIÇO DE ATENÇÃO A SAÚDE NO SISTEMA PENITENCIÁRIO"

        assert len(classifications) == 6
        assert classifications[2].id == 3
        assert classifications[2].service_id == 3
        assert classifications[2].code == "001"
        assert classifications[2].name == "ATENDIMENTO EM PRESÍDIO ATÉ 100 PRESOS"

        self._delete_classifications_from_db(ids=[3, 4, 5, 6])
        self._delete_services_from_db(ids=[3, 4])

    def test_upload_services_and_classifications_from_xlsx_file(
        self, post_services_and_classifications_with_file
    ):
        response = post_services_and_classifications_with_file(
            file_name="service_classification.xlsx"
        )

        assert response.json["message"] == "services_and_classifications_uploaded"
        assert response.status_code == 201

        services = Service.query.all()
        classifications = Classification.query.all()

        assert len(services) == 4
        assert services[2].id == 3
        assert services[2].code == "100"
        assert services[2].name == "SERVIÇO DE ATENÇÃO A SAÚDE NO SISTEMA PENITENCIÁRIO"

        assert len(classifications) == 6
        assert classifications[2].id == 3
        assert classifications[2].service_id == 3
        assert classifications[2].code == "001"
        assert classifications[2].name == "ATENDIMENTO EM PRESÍDIO ATÉ 100 PRESOS"

        self._delete_classifications_from_db(ids=[3, 4, 5, 6])
        self._delete_services_from_db(ids=[3, 4])

    def test_upload_service_classification_with_registered_data(
        self, post_services_and_classifications_with_file
    ):
        response = post_services_and_classifications_with_file(
            file_name="service_classification_unique_violation.xlsx"
        )

        assert response.status_code == 400
        assert response.json["message"] == "unique_violation"

    # --------------------- DELETE ---------------------

    def test_delete_classification(self, client):
        response = client.delete("/service/classification/1")

        assert response.status_code == 200
        assert response.json["message"] == "classification_deleted"

    def test_delete_classification_with_non_registered_id(self, client):
        response = client.delete("/service/classification/0")

        assert response.status_code == 404
        assert response.json["message"] == "classification_not_found"

    # --------------------- Helper functions  ---------------------

    def _undo_classification_update_changes(self) -> None:
        classification = Classification.query.get(1)

        classification.service_id = 1
        classification.code = "001"
        classification.name = "CLASSIFICATION ONE"

        db.session.commit()

    def _delete_classifications_from_db(self, ids: list[int]) -> None:
        Classification.query.filter(Classification.id.in_(ids)).delete()
        db.session.commit()

    def _delete_services_from_db(self, ids: list[int]) -> None:
        Service.query.filter(Service.id.in_(ids)).delete()
        db.session.commit()
