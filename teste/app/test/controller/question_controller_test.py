import pytest

from app.main import db
from app.test.seeders import (
    create_base_seed_diagnosis,
    create_base_seed_protocol,
    create_base_seed_question,
)


@pytest.fixture(scope="module")
def seeded_database(database):
    """Seed database with question data"""
    create_base_seed_question(db)
    create_base_seed_diagnosis(db)
    create_base_seed_protocol(db)


@pytest.mark.usefixtures("seeded_database")
class TestQuestionController:

    # --------------------- GET QUESTIONS ---------------------
    def test_get_questions(self, client):
        response = client.get("/question")

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 2
        assert response.json["total_pages"] == 1
        assert response.json["items"][0]["name"] == "PERGUNTA1"
        assert response.json["items"][0]["id"] == 1
        assert response.json["items"][1]["name"] == "PERGUNTA2"
        assert response.json["items"][1]["id"] == 2

    # --------------------- GET QUESTION BY ID ---------------------

    def test_get_question_by_id(self, client):
        response = client.get("/question/1")
        assert response.status_code == 200
        assert response.json["name"] == "PERGUNTA1"

    def test_get_question_with_wrong_id(self, client):
        response = client.get("/question/10")
        assert response.status_code == 404
        assert response.json["message"] == "question_not_found"

    # --------------------- UPDATE ---------------------

    def test_update_question_with_name_in_use(self, client):
        response = client.put("/question/1", json={"name": "pergunta1"})

        assert response.status_code == 409
        assert response.json["message"] == "name_in_use"

    def test_update_question_with_no_argument(self, client):
        response = client.post("/question", json={})

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"

    def test_update_question_with_invalid_id(self, client):
        response = client.put("/question/10", json={"name": "questão23"})

        assert response.status_code == 404
        assert response.json["message"] == "question_not_found"

    def test_update_question_with_empty_name(self, client):
        response = client.put("/question/1", json={"name": ""})

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert "name" in response.json["errors"].keys()

    def test_update_question(self, client):
        response = client.put("/question/1", json={"name": "questão23"})

        assert response.status_code == 200
        assert response.json["message"] == "question_updated"

    # --------------------- POST ---------------------

    def test_register_name_in_use(self, client):
        response = client.post("/question", json={"name": "questão23"})

        assert response.status_code == 409
        assert response.json["message"] == "name_in_use"

    def test_register_question_with_no_argument(self, client):
        response = client.post("/question", json={})

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"

    def test_register_question_with_invalid_format(self, client):
        response = client.post("/question", json={"name": 1})

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"

    def test_register_question_with_empty_name(self, client):
        response = client.post("/question", json={"name": ""})

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert "name" in response.json["errors"].keys()

    def test_register_question(self, client, base_question):
        response = client.post("/question", json=base_question)

        assert response.status_code == 201
        assert response.json["message"] == "question_created"

    # --------------------- DELETE ---------------------

    def test_delete_question_associated_with_diagnosis(self, client):
        response = client.delete("/question/1")

        assert response.status_code == 409
        assert response.json["message"] == "question_is_associated_with_diagnosis"

    def test_delete_question_with_invalid_id(seolf, client):
        response = client.delete("/question/10")

        assert response.status_code == 404
        assert response.json["message"] == "question_not_found"

    def test_delete_question_not_associated_with_diagnosis(self, client):
        response = client.delete("/question/2")

        assert response.status_code == 200
        assert response.json["message"] == "question_deleted"
