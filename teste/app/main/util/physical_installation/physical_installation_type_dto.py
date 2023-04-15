from flask_restx import Namespace, fields


class PhysicalInstallationTypeDTO:
    api = Namespace(
        "physical_installation",
        description="physical installation related operations",
    )

    physical_installation_type_post = api.model(
        "physical_installation_type_post",
        {
            "name": fields.String(
                required=True,
                description="physical installation type name",
                min_length=1,
            )
        },
    )

    physical_installation_type_put = api.clone(
        "physical_installation_type_put",
        physical_installation_type_post,
    )

    physical_installation_type_response = api.model(
        "physical_installation_type_response",
        {
            "id": fields.Integer(description="physical installation type id"),
            "name": fields.String(description="physical installation type name"),
        },
    )

    physical_installation_type_list = api.model(
        "physical_installation_type_list",
        {
            "current_page": fields.Integer(),
            "total_items": fields.Integer(),
            "total_pages": fields.Integer(),
            "items": fields.List(fields.Nested(physical_installation_type_response)),
        },
    )
