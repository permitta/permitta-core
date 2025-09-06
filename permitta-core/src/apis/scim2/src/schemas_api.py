from app_logger import Logger, get_logger
from flask import Blueprint, jsonify, make_response, request, Response

logger: Logger = get_logger("scim2.schemas_api")
bp = Blueprint("scim2_schemas", __name__, url_prefix="/api/scim/v2/Schemas")


@bp.route("", methods=["GET"])
def get_schemas():
    """
    Get the Schemas.

    This endpoint returns information about the schemas supported by the SCIM service provider.
    """
    schemas = {
        "schemas": ["urn:ietf:params:scim:api:messages:2.0:ListResponse"],
        "totalResults": 2,
        "Resources": [
            {
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
            },
            {
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
        ],
    }

    response: Response = make_response(
        jsonify(schemas),
    )
    response.headers["Content-Type"] = "application/scim+json"
    return response
