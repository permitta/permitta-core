from app_logger import Logger, get_logger
from flask import Blueprint, jsonify, make_response, request, Response

logger: Logger = get_logger("scim2.schemas_user_api")
bp = Blueprint(
    "scim2_schemas_user",
    __name__,
    url_prefix="/api/scim/v2/Schemas/urn:ietf:params:scim:schemas:core:2.0:User",
)


@bp.route("", methods=["GET"])
def get_user_schema():
    """
    Get the User Schema.

    This endpoint returns information about the User schema.
    """
    user_schema = {
        "id": "urn:ietf:params:scim:schemas:core:2.0:User",
        "name": "User",
        "description": "User Account",
        "attributes": [
            {
                "name": "id",
                "type": "string",
                "multiValued": False,
                "description": "Unique identifier for the User",
                "required": True,
                "caseExact": True,
                "mutability": "readOnly",
                "returned": "always",
                "uniqueness": "server",
            },
            {
                "name": "userName",
                "type": "string",
                "multiValued": False,
                "description": "Unique identifier for the User",
                "required": True,
                "caseExact": False,
                "mutability": "readWrite",
                "returned": "always",
                "uniqueness": "server",
            },
            {
                "name": "name",
                "type": "complex",
                "multiValued": False,
                "description": "The components of the user's name",
                "required": False,
                "subAttributes": [
                    {
                        "name": "formatted",
                        "type": "string",
                        "multiValued": False,
                        "description": "The full name, including all middle names, titles, and suffixes as appropriate",
                        "required": False,
                        "caseExact": False,
                        "mutability": "readWrite",
                        "returned": "default",
                        "uniqueness": "none",
                    },
                    {
                        "name": "givenName",
                        "type": "string",
                        "multiValued": False,
                        "description": "The given name of the User",
                        "required": False,
                        "caseExact": False,
                        "mutability": "readWrite",
                        "returned": "default",
                        "uniqueness": "none",
                    },
                    {
                        "name": "familyName",
                        "type": "string",
                        "multiValued": False,
                        "description": "The family name of the User",
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
            {
                "name": "emails",
                "type": "complex",
                "multiValued": True,
                "description": "Email addresses for the user",
                "required": False,
                "subAttributes": [
                    {
                        "name": "value",
                        "type": "string",
                        "multiValued": False,
                        "description": "Email address value",
                        "required": False,
                        "caseExact": False,
                        "mutability": "readWrite",
                        "returned": "default",
                        "uniqueness": "none",
                    },
                    {
                        "name": "type",
                        "type": "string",
                        "multiValued": False,
                        "description": "A label indicating the attribute's function, e.g., 'work' or 'home'",
                        "required": False,
                        "caseExact": False,
                        "canonicalValues": ["work", "home", "other"],
                        "mutability": "readWrite",
                        "returned": "default",
                        "uniqueness": "none",
                    },
                    {
                        "name": "primary",
                        "type": "boolean",
                        "multiValued": False,
                        "description": "A Boolean value indicating the 'primary' or preferred attribute value",
                        "required": False,
                        "mutability": "readWrite",
                        "returned": "default",
                        "uniqueness": "none",
                    },
                ],
                "mutability": "readWrite",
                "returned": "default",
                "uniqueness": "none",
            },
            {
                "name": "active",
                "type": "boolean",
                "multiValued": False,
                "description": "A Boolean value indicating the User's administrative status",
                "required": False,
                "mutability": "readWrite",
                "returned": "default",
                "uniqueness": "none",
            },
        ],
        "meta": {
            "resourceType": "Schema",
            "location": "/Schemas/urn:ietf:params:scim:schemas:core:2.0:User",
        },
    }

    response: Response = make_response(
        jsonify(user_schema),
    )
    response.headers["Content-Type"] = "application/scim+json"
    return response
