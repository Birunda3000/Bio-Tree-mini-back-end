import pytest

from app.main import db
from app.test.seeders import (
    create_base_seed_admission,
    create_base_seed_clinical_evolution,
    create_base_seed_medical_prescription,
    create_base_seed_professional,
)


@pytest.fixture(scope="module")
def seeded_database(client, database):
    """Seed database with clinical evolution data"""
    create_base_seed_professional(db)
    create_base_seed_medical_prescription(db)
    create_base_seed_admission(db)
    create_base_seed_clinical_evolution(db)


@pytest.mark.usefixtures("seeded_database")
class TestClinicalEvolutionController:

    # --------------------- CREATE CLINICAL_EVOLUTION ---------------------

    @pytest.mark.parametrize(
        "remove_data",
        [
            (["medical_prescription_medicines_data"]),
            (["medical_prescription_orientations_data"]),
            (["medical_prescription_procedures_data"]),
            (
                [
                    "medical_prescription_medicines_data",
                    "medical_prescription_orientations_data",
                ]
            ),
            (
                [
                    "medical_prescription_medicines_data",
                    "medical_prescription_procedures_data",
                ]
            ),
            (
                [
                    "medical_prescription_orientations_data",
                    "medical_prescription_procedures_data",
                ]
            ),
        ],
    )
    def test_create_clinical_evolution(
        self,
        client,
        base_clinical_evolution_history,
        remove_data,
    ):
        for data in remove_data:
            base_clinical_evolution_history.pop(data)

        response = client.post(
            "/clinical_evolution", json=base_clinical_evolution_history
        )

        assert response.status_code == 201
        assert response.json["message"] == "clinical_evolution_created"

    @pytest.mark.parametrize(
        "key_popped",
        [
            ("admission_id"),
            ("professional_id"),
        ],
        ids=[
            "without_admission_id",
            "without_professional_id",
        ],
    )
    def test_create_clinical_evolution_without_required_dto_data(
        self, client, base_clinical_evolution_history, key_popped
    ):

        base_clinical_evolution_history.pop(key_popped, None)

        response = client.post(
            "/clinical_evolution", json=base_clinical_evolution_history
        )

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert key_popped in response.json["errors"].keys()

    @pytest.mark.parametrize(
        "key_popped",
        [
            ("id"),
            ("operation_type"),
            ("performed_at"),
        ],
        ids=[
            "without_medical_prescription_medicine_id",
            "without_medical_prescription_medicine_operation_type",
            "without_medical_prescription_medicine_performed_at",
        ],
    )
    def test_create_clinical_evolution_without_required_medical_prescription_medicine_dto_data(
        self, client, base_clinical_evolution_history, key_popped
    ):

        base_clinical_evolution_history["medical_prescription_medicines_data"][0].pop(
            key_popped, None
        )

        response = client.post(
            "/clinical_evolution", json=base_clinical_evolution_history
        )

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert (
            f"medical_prescription_medicines_data.0.{key_popped}"
            in response.json["errors"].keys()
        )

    @pytest.mark.parametrize(
        "key_popped",
        [
            ("id"),
            ("operation_type"),
            ("performed_at"),
        ],
        ids=[
            "without_medical_prescription_orientation_id",
            "without_medical_prescription_orientation_operation_type",
            "without_medical_prescription_orientation_performed_at",
        ],
    )
    def test_create_clinical_evolution_without_required_medical_prescription_orientation_dto_data(
        self, client, base_clinical_evolution_history, key_popped
    ):

        base_clinical_evolution_history["medical_prescription_orientations_data"][
            0
        ].pop(key_popped, None)

        response = client.post(
            "/clinical_evolution", json=base_clinical_evolution_history
        )

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert (
            f"medical_prescription_orientations_data.0.{key_popped}"
            in response.json["errors"].keys()
        )

    @pytest.mark.parametrize(
        "key_popped",
        [
            ("id"),
            ("operation_type"),
            ("performed_at"),
        ],
        ids=[
            "without_medical_prescription_orientation_id",
            "without_medical_prescription_procedure_operation_type",
            "without_medical_prescription_procedure_performed_at",
        ],
    )
    def test_create_clinical_evolution_without_required_medical_prescription_procedure_dto_data(
        self, client, base_clinical_evolution_history, key_popped
    ):

        base_clinical_evolution_history["medical_prescription_procedures_data"][0].pop(
            key_popped, None
        )

        response = client.post(
            "/clinical_evolution", json=base_clinical_evolution_history
        )

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert (
            f"medical_prescription_procedures_data.0.{key_popped}"
            in response.json["errors"].keys()
        )

    def test_create_clinical_evolution_without_required_data(
        self,
        client,
        base_clinical_evolution_history,
    ):

        remove_data = [
            "medical_prescription_medicines_data",
            "medical_prescription_orientations_data",
            "medical_prescription_procedures_data",
        ]
        for data in remove_data:
            base_clinical_evolution_history.pop(data)

        response = client.post(
            "/clinical_evolution", json=base_clinical_evolution_history
        )

        assert response.status_code == 404
        assert response.json["message"] == "clinical_evolution_data_not_found"

    @pytest.mark.parametrize(
        "key,new_value,expected_message",
        [
            ("professional_id", 0, "professional_not_found"),
            ("admission_id", 0, "admission_not_found"),
        ],
        ids=["invalid_professional_id", "invalid_admission_id"],
    )
    def test_create_clinical_evolution_with_invalid_data(
        self, client, base_clinical_evolution_history, key, new_value, expected_message
    ):
        base_clinical_evolution_history[key] = new_value
        response = client.post(
            "/clinical_evolution", json=base_clinical_evolution_history
        )

        assert response.status_code == 404
        assert response.json["message"] == expected_message

    @pytest.mark.parametrize(
        "key,expected_message",
        [
            (
                "medical_prescription_medicines_data",
                "medical_prescription_medicine_not_found",
            ),
            (
                "medical_prescription_orientations_data",
                "medical_prescription_orientation_not_found",
            ),
            (
                "medical_prescription_procedures_data",
                "medical_prescription_procedure_not_found",
            ),
        ],
        ids=["invalid_medicine_id", "invalid_orientation_id", "invalid_procedure_id"],
    )
    def test_create_clinical_evolution_with_invalid_medical_prescription_data(
        self, client, base_clinical_evolution_history, key, expected_message
    ):
        base_clinical_evolution_history[key][0]["id"] = 0
        response = client.post(
            "/clinical_evolution", json=base_clinical_evolution_history
        )

        assert response.status_code == 404
        assert response.json["message"] == expected_message
