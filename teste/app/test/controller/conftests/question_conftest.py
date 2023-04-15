import pytest


@pytest.fixture()
def base_question():
    """Base question"""
    question = {"name": "questão1"}

    return question
