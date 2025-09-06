from app_logger import Logger, get_logger
from flask import Blueprint, jsonify, make_response, request, Response

logger: Logger = get_logger("scim2.schemas_group_api")
bp = Blueprint(
    "scim2_schemas_group",
    __name__,
    url_prefix="/api/scim/v2/Schemas/urn:ietf:params:scim:schemas:core:2.0:Group",
)


@bp.route("", methods=["GET"])
def get_group_schema():
    """
    Get the Group Schema.

    This endpoint returns information about the Group schema.
    """
    group_schema = {
        "id": "urn:ietf:params:scim:schemas:core:2.0:Group",
        "name": "Group",
        "description": "Group",
        "attributes": [
            {
                "name": "id",
                "type": "string",
                "multiValued": False,
                "description": "Unique identifier for the Group",
                "required": True,
                "caseExact": True,
                "mutability": "readOnly",
                "returned": "always",
                "uniqueness": "server",
            },
            {
                "name": "displayName",
                "type": "string",
                "multiValued": False,
                "description": "A human-readable name for the Group",
                "required": True,
                "caseExact": False,
                "mutability": "readWrite",
                "returned": "always",
                "uniqueness": "server",
            },
            {
                "name": "members",
                "type": "complex",
                "multiValued": True,
                "description": "A list of members of the Group",
                "required": False,
                "subAttributes": [
                    {
                        "name": "value",
                        "type": "string",
                        "multiValued": False,
                        "description": "Identifier of the member of this Group",
                        "required": True,
                        "caseExact": False,
                        "mutability": "readWrite",
                        "returned": "default",
                        "uniqueness": "none",
                    },
                    {
                        "name": "type",
                        "type": "string",
                        "multiValued": False,
                        "description": "A label indicating the type of resource, e.g., 'User' or 'Group'",
                        "required": False,
                        "caseExact": False,
                        "canonicalValues": ["User", "Group"],
                        "mutability": "readWrite",
                        "returned": "default",
                        "uniqueness": "none",
                    },
                    {
                        "name": "$ref",
                        "type": "reference",
                        "multiValued": False,
                        "description": "The URI of the corresponding resource",
                        "required": False,
                        "caseExact": False,
                        "mutability": "readWrite",
                        "returned": "default",
                        "uniqueness": "none",
                        "referenceTypes": ["User", "Group"],
                    },
                    {
                        "name": "display",
                        "type": "string",
                        "multiValued": False,
                        "description": "A human-readable name for the member",
                        "required": False,
                        "caseExact": False,
                        "mutability": "readWrite",
                        "returned": "default",
                        "uniqueness": "none",
                    },
                ],
                "mutability": "readWrite",
                "returned": "default",
                "uniqueness": "none",
            },
        ],
        "meta": {
            "resourceType": "Schema",
            "location": "/Schemas/urn:ietf:params:scim:schemas:core:2.0:Group",
        },
    }

    response: Response = make_response(
        jsonify(group_schema),
    )
    response.headers["Content-Type"] = "application/scim+json"
    return response