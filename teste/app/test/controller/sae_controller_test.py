import pytest

from app.main import db
from app.test.seeders import (
    create_base_seed_action,
    create_base_seed_admission,
    create_base_seed_admission_action_association,
    create_base_seed_admission_question_association,
    create_base_seed_professional,
    create_base_seed_question,
)


@pytest.fixture(scope="module")
def seeded_database(client, database):
    """Seed database with sae data"""

    create_base_seed_professional(db)
    create_base_seed_admission(db)
    create_base_seed_action(db)
    create_base_seed_question(db)
    create_base_seed_admission_question_association(db)
    create_base_seed_admission_action_association(db)


@pytest.mark.usefixtures("seeded_database")
class TesteSaeController:

    # --------------------- GET BY ADMISSION ---------------------
    def teste_get_sae(self, client):
        response = response = client.get("/sae", query_string={"admission_id": 1})
        assert response.status_code == 200
        assert len(response.json) == 2
        assert len(response.json["questions"]) == 2
        assert len(response.json["actions"]) == 2
        assert response.json["questions"][0]["id"] == 1
        assert response.json["questions"][0]["name"] == "PERGUNTA1"
        assert response.json["questions"][1]["id"] == 2
        assert response.json["questions"][1]["name"] == "PERGUNTA2"
        assert response.json["actions"][0]["id"] == 1
        assert response.json["actions"][0]["name"] == "AÇÃO TESTE 1"
        assert response.json["actions"][0]["recurrence"] == "1/1"
        assert response.json["actions"][1]["id"] == 2
        assert response.json["actions"][1]["name"] == "AÇÃO TESTE 2"
        assert response.json["actions"][1]["recurrence"] == "2/2"

    def test_get_sae_by_non_registered_admission(self, client):
        response = client.get("/sae", query_string={"admission_id": 0})
        assert response.status_code == 404
        assert response.json["message"] == "admission_not_found"

    # --------------------- POST PERFORM SAE ---------------------

    def test_register_sae_perform_with_non_registered_admission(
        self, client, base_sae_perform
    ):
        base_sae_perform["admission_id"] = 0
        response = client.post("/sae", json=base_sae_perform)

        assert response.status_code == 404
        assert response.json["message"] == "admission_not_found"

    def test_register_sae_perform_with_non_registered_professional(
        self, client, base_sae_perform
    ):
        base_sae_perform["professional_id"] = 0
        response = client.post("/sae", json=base_sae_perform)

        assert response.status_code == 404
        assert response.json["message"] == "professional_not_found"

    def test_register_sae_perform_with_non_registered_action(
        self, client, base_sae_perform
    ):
        base_sae_perform["prescriptions_performed"][0]["action_id"] = 0
        response = client.post("/sae", json=base_sae_perform)

        assert response.status_code == 404
        assert response.json["message"] == "action_not_found"

    def test_register_sae_perform_with_non_associated_action(
        self, client, base_sae_perform
    ):
        base_sae_perform["prescriptions_performed"][0]["action_id"] = 3
        response = client.post("/sae", json=base_sae_perform)

        assert response.status_code == 404
        assert response.json["message"] == "action_not_found"

    @pytest.mark.parametrize(
        "key_popped",
        ["admission_id", "professional_id"],
        ids=[
            "register_without_vital_signs_control",
            "register_without_prescriptions_performed",
        ],
    )
    def test_register_sae_perform_without_required_data(
        self, client, base_sae_perform, key_popped
    ):
        base_sae_perform.pop(key_popped, None)
        response = client.post("/sae", json=base_sae_perform)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert key_popped in response.json["errors"].keys()

    @pytest.mark.parametrize(
        "key_popped",
        [
            "sys_blood_pressure",
            "dia_blood_pressure",
            "heart_pulse",
            "respiratory_frequence",
            "body_fat_rate",
            "performed_at",
        ],
        ids=[
            "register_without_sys_blood_pressure",
            "register_without_dia_blood_pressure",
            "register_without_heart_pulse",
            "register_without_respiratory_frequence",
            "register_without_body_fat_rate",
            "register_without_performed_at",
        ],
    )
    def test_register_sae_perform_without_required_data_for_vital_signs_control(
        self, client, base_sae_perform, key_popped
    ):

        base_sae_perform["vital_signs_control"].pop(key_popped, None)
        response = client.post("/sae", json=base_sae_perform)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert f"vital_signs_control.{key_popped}" in response.json["errors"].keys()

    @pytest.mark.parametrize(
        "key_popped",
        [
            "action_id",
            "performed_at",
            "delete",
        ],
        ids=[
            "register_without_action_id",
            "register_without_performed_at",
            "register_without_delete",
        ],
    )
    def test_register_sae_perform_without_required_data_for_prescriptions_performed(
        self, client, base_sae_perform, key_popped
    ):

        base_sae_perform["prescriptions_performed"][0].pop(key_popped, None)
        response = client.post("/sae", json=base_sae_perform)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert (
            f"prescriptions_performed.0.{key_popped}" in response.json["errors"].keys()
        )

    def test_register_sae_perform_without_vital_signs_control_and_prescriptions_performed(
        self, client, base_sae_perform
    ):
        base_sae_perform.pop("vital_signs_control")
        base_sae_perform.pop("prescriptions_performed")
        response = client.post("/sae", json=base_sae_perform)

        assert response.status_code == 409
        assert response.json["message"] == "informations_empty"

    def test_register_sae_perform_with_prescriptions_performed_empty(
        self, client, base_sae_perform
    ):
        base_sae_perform["prescriptions_performed"]
        response = client.post("/sae", json=base_sae_perform)

        assert response.status_code == 201
        assert response.json["message"] == "sae_performed"

    def test_register_sae_perform_without_vital_signs_control(
        self, client, base_sae_perform
    ):
        base_sae_perform.pop("vital_signs_control")
        response = client.post("/sae", json=base_sae_perform)

        assert response.status_code == 201
        assert response.json["message"] == "sae_performed"

    def test_register_sae_perform_without_prescriptions_performed(
        self, client, base_sae_perform
    ):
        base_sae_perform.pop("prescriptions_performed")
        response = client.post("/sae", json=base_sae_perform)

        assert response.status_code == 201
        assert response.json["message"] == "sae_performed"

    def test_register_sae_perform(self, client, base_sae_perform):
        response = client.post("/sae", json=base_sae_perform)

        assert response.status_code == 201
        assert response.json["message"] == "sae_performed"

    def test_register_sae_perform_with_prescriptions_perfomed_field_delete_equal_true(
        self, client, base_sae_perform
    ):
        base_sae_perform["prescriptions_performed"][0]["delete"] = True
        response = client.post("/sae", json=base_sae_perform)

        assert response.status_code == 201
        assert response.json["message"] == "sae_performed"

    # --------------------- POST SAE DETERMINATIONS ---------------------

    @pytest.mark.parametrize(
        "key_popped",
        ["admission_id", "professional_id", "actions", "questions"],
        ids=[
            "register_without_admission_id",
            "register_without_professional_id",
            "register_without_actions",
            "register_without_questions",
        ],
    )
    def test_register_sae_determinations_without_required_data(
        self, client, base_sae_determinations, key_popped
    ):
        base_sae_determinations.pop(key_popped, None)
        response = client.post("/sae/determinations", json=base_sae_determinations)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert key_popped in response.json["errors"].keys()

    @pytest.mark.parametrize(
        "key_popped",
        ["id", "recurrence"],
        ids=[
            "register_without_action_id",
            "register_without_action_recurrence",
        ],
    )
    def test_register_sae_determinations_without_required_data_for_actions(
        self, client, base_sae_determinations, key_popped
    ):
        base_sae_determinations["actions"][0].pop(key_popped, None)

        response = client.post("/sae/determinations", json=base_sae_determinations)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert f"actions.0.{key_popped}" in response.json["errors"].keys()

    def test_register_sae_determinations_with_non_registered_admission(
        self, client, base_sae_determinations
    ):
        base_sae_determinations["admission_id"] = 123
        response = client.post("/sae/determinations", json=base_sae_determinations)
        assert response.status_code == 404
        assert response.json["message"] == "admission_not_found"

    def test_register_sae_determinations_with_non_registered_professional(
        self, client, base_sae_determinations
    ):
        base_sae_determinations["professional_id"] = 123
        response = client.post("/sae/determinations", json=base_sae_determinations)
        assert response.status_code == 404
        assert response.json["message"] == "professional_not_found"

    def test_register_sae_determinations_with_non_registered_action(
        self, client, base_sae_determinations
    ):
        base_sae_determinations["actions"][0]["id"] = 123
        response = client.post("/sae/determinations", json=base_sae_determinations)
        assert response.status_code == 404
        assert response.json["message"] == "action_not_found"

    def test_register_sae_determinations_with_non_registered_question(
        self, client, base_sae_determinations
    ):
        base_sae_determinations["questions"] = [0, 123]
        response = client.post("/sae/determinations", json=base_sae_determinations)
        assert response.status_code == 404
        assert response.json["message"] == "question_not_found"

    def test_register_sae_determinations_with_actions_and_questions_empty(
        self, client, base_sae_determinations
    ):
        base_sae_determinations["actions"] = []
        base_sae_determinations["questions"] = []
        response = client.post("/sae/determinations", json=base_sae_determinations)
        assert response.status_code == 409
        assert response.json["message"] == "determinations_empty"

    def test_register_sae_determinations(self, client, base_sae_determinations):
        response = client.post("/sae/determinations", json=base_sae_determinations)

        assert response.status_code == 201
        assert response.json["message"] == "determinations_created"

    # --------------------- DELETE SAE QUESTIONS ---------------------

    def test_delete_sae_questions_with_questions_empty(self, client):
        response = client.delete(
            "/sae/questions",
            json={
                "admission_id": 1,
                "professional_id": 1,
                "questions": [],
            },
        )
        assert response.status_code == 409
        assert response.json["message"] == "questions_empty"

    def test_delete_sae_questions_by_non_registered_admission(self, client):
        response = client.delete(
            "/sae/questions",
            json={
                "admission_id": 123,
                "professional_id": 1,
                "questions": [1, 2],
            },
        )
        assert response.status_code == 404
        assert response.json["message"] == "admission_not_found"

    def test_delete_sae_questions_by_non_registered_professional(self, client):
        response = client.delete(
            "/sae/questions",
            json={
                "admission_id": 1,
                "professional_id": 123,
                "questions": [1, 2],
            },
        )
        assert response.status_code == 404
        assert response.json["message"] == "professional_not_found"

    def test_delete_sae_questions_by_non_registered_question(self, client):
        response = client.delete(
            "/sae/questions",
            json={
                "admission_id": 1,
                "professional_id": 1,
                "questions": [123, 2],
            },
        )
        assert response.status_code == 404
        assert response.json["message"] == "question_not_found"

    @pytest.mark.parametrize(
        "key_popped",
        ["admission_id", "professional_id", "questions"],
        ids=[
            "register_without_admission_id",
            "register_without_professional_id",
            "register_without_questions",
        ],
    )
    def test_register_sae_determinations_without_required_data(
        self, client, base_sae_determinations, key_popped
    ):
        base_sae_determinations.pop(key_popped, None)
        response = client.delete("/sae/questions", json=base_sae_determinations)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert key_popped in response.json["errors"].keys()

    def test_delete_sae_questions(self, client):
        response = client.delete(
            "/sae/questions",
            json={
                "admission_id": 1,
                "professional_id": 1,
                "questions": [1, 2],
            },
        )
        assert response.status_code == 200
        assert response.json["message"] == "questions_deleted"
