from flask_restx import Namespace, fields


class PhysicalInstallationSubtypeDTO:
    api = Namespace(
        "physical_installation_subtype",
        description="physical installation subtype related operations",
    )

    physical_installation_subtype_post = api.model(
        "physical_installation_subtype_post",
        {
            "name": fields.String(
                required=True,
                description="physical installation subtype name",
                min_length=1,
            ),
        },
    )

    physical_installation_subtype_put = api.clone(
        "physical_installation_subtype_put",
        physical_installation_subtype_post,
    )

    physical_installation_subtype_response = api.model(
        "physical_installation_subtype_response",
        {
            "id": fields.Integer(description="physical installation subtype id"),
            "name": fields.String(description="physical installation subtype name"),
        },
    )

    physical_installation_subtype_list = api.model(
        "physical_installation_subtype_list",
        {
            "current_page": fields.Integer(),
            "total_items": fields.Integer(),
            "total_pages": fields.Integer(),
            "items": fields.List(fields.Nested(physical_installation_subtype_response)),
        },
    )
