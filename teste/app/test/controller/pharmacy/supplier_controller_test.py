import pytest

from app.main import db
from app.main.model import Supplier
from app.test.seeders import create_base_seed_supplier


@pytest.fixture(scope="module")
def seeded_database(client, database):
    """Seed database with prescription data"""

    create_base_seed_supplier(db)


@pytest.mark.usefixtures("seeded_database")
class TestSupplierController:

    # --------------------- GET  ---------------------

    def test_get_suppliers(self, client):
        response = client.get("/supplier")

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 3
        assert response.json["total_pages"] == 1
        assert response.json["items"][0]["id"] == 1
        assert response.json["items"][0]["name"] == "SUPPLIER 1"
        assert response.json["items"][0]["cpf"] == "67179848050"
        assert response.json["items"][1]["id"] == 2
        assert response.json["items"][1]["name"] == "SUPPLIER 2"
        assert response.json["items"][1]["cnpj"] == "13504619000185"
        assert response.json["items"][2]["id"] == 3
        assert response.json["items"][2]["name"] == "SUPPLIER 3"
        assert response.json["items"][2]["cpf"] == "84928321006"

    @pytest.mark.parametrize(
        "key, value",
        [
            ("name", "SUPPLIER 1"),
            ("cpf", "84928321006"),
            ("cnpj", "13504619000185"),
        ],
        ids=[
            "name",
            "cpf",
            "cnpj",
        ],
    )
    def test_get_suppliers_by(self, client, key, value):
        response = client.get("/supplier", query_string={key: value})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 1
        assert response.json["total_pages"] == 1
        assert response.json["items"][0][key] == value

    def test_get_suppliers_by_legal_person_only(self, client):
        response = client.get("/supplier", query_string={"legal_person": "true"})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 1
        assert response.json["total_pages"] == 1
        assert response.json["items"][0]["id"] == 2
        assert response.json["items"][0]["name"] == "SUPPLIER 2"
        assert response.json["items"][0]["cnpj"] == "13504619000185"

    def test_get_suppliers_by_natural_person_only(self, client):
        response = client.get("/supplier", query_string={"legal_person": "false"})

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 2
        assert response.json["total_pages"] == 1
        assert response.json["items"][0]["id"] == 1
        assert response.json["items"][0]["name"] == "SUPPLIER 1"
        assert response.json["items"][0]["cpf"] == "67179848050"
        assert response.json["items"][1]["id"] == 3
        assert response.json["items"][1]["name"] == "SUPPLIER 3"
        assert response.json["items"][1]["cpf"] == "84928321006"

    # --------------------- GET BY ID ---------------------

    def test_get_supplier(self, client):
        response = client.get("/supplier/1")

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["id"] == 1
        assert response.json["name"] == "SUPPLIER 1"
        assert response.json["cpf"] == "67179848050"

    def test_get_supplier_that_not_exists(self, client):
        response = client.get("/supplier/0")

        assert response.json["message"] == "supplier_not_found"
        assert response.status_code == 404

    # --------------------- UPDATE ---------------------

    @pytest.mark.parametrize(
        "key_popped",
        [
            "name",
        ],
        ids=[
            "without_name",
        ],
    )
    def test_update_supplier_without_required_data(
        self, client, base_supplier, key_popped
    ):
        base_supplier.pop(key_popped, None)
        response = client.put("/supplier/2", json=base_supplier)

        assert response.json["message"] == "Input payload validation failed"
        assert response.status_code == 400
        assert key_popped in response.json["errors"].keys()

    @pytest.mark.parametrize(
        "key, value",
        [
            ("name", 0),
            ("name", ""),
        ],
        ids=[
            "with_invalid_name",
            "with_empty_name",
        ],
    )
    def test_update_supplier_with_invalid_data(self, client, base_supplier, key, value):
        base_supplier[key] = value
        response = client.put("/supplier/1", json=base_supplier)

        assert response.json["message"] == "Input payload validation failed"
        assert response.status_code == 400
        assert key in response.json["errors"].keys()

    def test_update_supplier_that_not_exists(self, client, base_supplier):
        response = client.put("/supplier/0", json=base_supplier)

        assert response.json["message"] == "supplier_not_found"
        assert response.status_code == 404

    def test_update_supplier(self, client, base_supplier):
        response = client.put("/supplier/1", json=base_supplier)

        assert response.json["message"] == "supplier_updated"
        assert response.status_code == 200

        supplier = Supplier.query.get(1)

        for key in base_supplier.keys():
            assert getattr(supplier, key) == base_supplier.get(key)

    # --------------------- POST AS NATURAL PERSON ---------------------

    @pytest.mark.parametrize(
        "key_popped",
        [
            "name",
            "cpf",
        ],
        ids=[
            "without_name",
            "without_cpf",
        ],
    )
    def test_create_supplier_as_natural_person_without_required_data(
        self, client, base_supplier_as_natural_person, key_popped
    ):
        base_supplier_as_natural_person.pop(key_popped, None)
        response = client.post(
            "/supplier/natural_person", json=base_supplier_as_natural_person
        )

        assert response.json["message"] == "Input payload validation failed"
        assert response.status_code == 400
        assert key_popped in response.json["errors"].keys()

    @pytest.mark.parametrize(
        "key, value",
        [
            ("name", 0),
            ("name", ""),
        ],
        ids=[
            "with_invalid_name",
            "with_empty_name",
        ],
    )
    def test_create_supplier_as_natural_person_with_invalid_data(
        self, client, base_supplier_as_natural_person, key, value
    ):
        base_supplier_as_natural_person[key] = value
        response = client.post(
            "/supplier/natural_person", json=base_supplier_as_natural_person
        )

        assert response.json["message"] == "Input payload validation failed"
        assert response.status_code == 400
        assert key in response.json["errors"].keys()

    @pytest.mark.parametrize(
        "key, value",
        [
            ("name", "SUPPLIER 3"),
            ("cpf", "84928321006"),
        ],
        ids=[
            "registered_name",
            "registered_cpf",
        ],
    )
    def test_create_supplier_as_natural_person_with_registered_data(
        self, client, base_supplier_as_natural_person, key, value
    ):
        base_supplier_as_natural_person[key] = value
        response = client.post(
            "/supplier/natural_person", json=base_supplier_as_natural_person
        )

        assert response.json["message"] == f"{key}_in_use"
        assert response.status_code == 409

    def test_create_supplier_as_natural_person(
        self, client, base_supplier_as_natural_person
    ):
        response = client.post(
            "/supplier/natural_person", json=base_supplier_as_natural_person
        )

        assert response.json["message"] == "supplier_created"
        assert response.status_code == 201

        supplier = Supplier.query.order_by(Supplier.id.desc()).first()

        for key in base_supplier_as_natural_person.keys():
            assert getattr(supplier, key) == base_supplier_as_natural_person.get(key)

    # --------------------- POST AS LEGAL PERSON ---------------------

    @pytest.mark.parametrize(
        "key_popped",
        [
            "name",
            "cnpj",
        ],
        ids=[
            "without_name",
            "without_cnpj",
        ],
    )
    def test_create_supplier_as_legal_person_without_required_data(
        self, client, base_supplier_as_legal_person, key_popped
    ):
        base_supplier_as_legal_person.pop(key_popped, None)
        response = client.post(
            "/supplier/legal_person", json=base_supplier_as_legal_person
        )

        assert response.json["message"] == "Input payload validation failed"
        assert response.status_code == 400
        assert key_popped in response.json["errors"].keys()

    @pytest.mark.parametrize(
        "key, value",
        [
            ("name", 0),
            ("name", ""),
        ],
        ids=[
            "create_with_invalid_name",
            "create_with_empty_name",
        ],
    )
    def test_create_supplier_as_legal_person_with_invalid_data(
        self, client, base_supplier_as_legal_person, key, value
    ):
        base_supplier_as_legal_person[key] = value
        response = client.post(
            "/supplier/legal_person", json=base_supplier_as_legal_person
        )

        assert response.json["message"] == "Input payload validation failed"
        assert response.status_code == 400
        assert key in response.json["errors"].keys()

    @pytest.mark.parametrize(
        "key, value",
        [
            ("name", "SUPPLIER 2"),
            ("cnpj", "13504619000185"),
        ],
        ids=[
            "registered_name",
            "registered_cnpj",
        ],
    )
    def test_create_supplier_as_legal_person_with_registered_data(
        self, client, base_supplier_as_legal_person, key, value
    ):
        base_supplier_as_legal_person[key] = value
        response = client.post(
            "/supplier/legal_person", json=base_supplier_as_legal_person
        )

        assert response.json["message"] == f"{key}_in_use"
        assert response.status_code == 409

    def test_create_supplier_as_legal_person(
        self, client, base_supplier_as_legal_person
    ):
        response = client.post(
            "/supplier/legal_person", json=base_supplier_as_legal_person
        )

        assert response.json["message"] == "supplier_created"
        assert response.status_code == 201

        supplier = Supplier.query.order_by(Supplier.id.desc()).first()

        for key in base_supplier_as_legal_person.keys():
            assert getattr(supplier, key) == base_supplier_as_legal_person.get(key)

    # --------------------- DELETE ---------------------

    def test_delete_institution_with_non_registered_id(self, client):
        response = client.delete("/supplier/0")

        assert response.json["message"] == "supplier_not_found"
        assert response.status_code == 404

    def test_delete_supplier(self, client):
        response = client.delete("/supplier/1")

        assert response.json["message"] == "supplier_deleted"
        assert response.status_code == 200
