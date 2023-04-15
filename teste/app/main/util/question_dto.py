from flask_restx import Namespace, fields


class QuestionDTO:
    api = Namespace("question", description="question related operations")

    question_name = api.model(
        "question_name",
        {
            "name": fields.String(description="question name"),
        },
    )

    question_post = api.model(
        "question_create",
        {
            "name": fields.String(
                required=True, description="question name", min_length=1
            )
        },
    )

    question_response = api.clone(
        "question_response",
        question_post,
        {"id": fields.Integer(description="question id")},
    )

    question_response_with_no_id = api.clone("question_response", question_post)

    question_list = api.model(
        "question_list",
        {
            "current_page": fields.Integer(),
            "total_items": fields.Integer(),
            "total_pages": fields.Integer(),
            "items": fields.List(fields.Nested(question_response)),
        },
    )
