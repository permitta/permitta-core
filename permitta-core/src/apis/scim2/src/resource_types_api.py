from app_logger import Logger, get_logger
from flask import Blueprint, jsonify, make_response, request, Response

logger: Logger = get_logger("scim2.resource_types_api")
bp = Blueprint(
    "scim2_resource_types", __name__, url_prefix="/api/scim/v2/ResourceTypes"
)


@bp.route("", methods=["GET"])
def get_resource_types():
    """
    Get the Resource Types.

    This endpoint returns information about the resource types supported by the SCIM service provider.
    """
    resource_types = {
        "schemas": ["urn:ietf:params:scim:api:messages:2.0:ListResponse"],
        "totalResults": 2,
        "Resources": [
            {
                "schemas": ["urn:ietf:params:scim:schemas:core:2.0:ResourceType"],
                "id": "User",
                "name": "User",
                "endpoint": "/Users",
                "description": "User Account",
                "schema": "urn:ietf:params:scim:schemas:core:2.0:User",
                "schemaExtensions": [],
                "meta": {
                    "location": "/ResourceTypes/User",
                    "resourceType": "ResourceType",
                    "created": "2023-01-01T00:00:00Z",
                    "lastModified": "2023-01-01T00:00:00Z",
                    "version": 'W/"1"',
                },
            },
            {
                "schemas": ["urn:ietf:params:scim:schemas:core:2.0:ResourceType"],
                "id": "Group",
                "name": "Group",
                "endpoint": "/Groups",
                "description": "Group",
                "schema": "urn:ietf:params:scim:schemas:core:2.0:Group",
                "schemaExtensions": [],
                "meta": {
                    "location": "/ResourceTypes/Group",
                    "resourceType": "ResourceType",
                    "created": "2023-01-01T00:00:00Z",
                    "lastModified": "2023-01-01T00:00:00Z",
                    "version": 'W/"1"',
                },
            },
        ],
    }

    response: Response = make_response(
        jsonify(resource_types),
    )
    response.headers["Content-Type"] = "application/scim+json"
    return response


@bp.route("/User", methods=["GET"])
def get_resource_type_user():
    """
    Get the User Resource Type.

    This endpoint returns information about the User resource type.
    """
    resource_type = {
        "schemas": ["urn:ietf:params:scim:schemas:core:2.0:ResourceType"],
        "id": "User",
        "name": "User",
        "endpoint": "/Users",
        "description": "User Account",
        "schema": "urn:ietf:params:scim:schemas:core:2.0:User",
        "schemaExtensions": [],
        "meta": {
            "location": "/ResourceTypes/User",
            "resourceType": "ResourceType",
            "created": "2023-01-01T00:00:00Z",
            "lastModified": "2023-01-01T00:00:00Z",
            "version": 'W/"1"',
        },
    }

    response: Response = make_response(
        jsonify(resource_type),
    )
    response.headers["Content-Type"] = "application/scim+json"
    return response


@bp.route("/Group", methods=["GET"])
def get_resource_type_group():
    """
    Get the Group Resource Type.

    This endpoint returns information about the Group resource type.
    """
    resource_type = {
        "schemas": ["urn:ietf:params:scim:schemas:core:2.0:ResourceType"],
        "id": "Group",
        "name": "Group",
        "endpoint": "/Groups",
        "description": "Group",
        "schema": "urn:ietf:params:scim:schemas:core:2.0:Group",
        "schemaExtensions": [],
        "meta": {
            "location": "/ResourceTypes/Group",
            "resourceType": "ResourceType",
            "created": "2023-01-01T00:00:00Z",
            "lastModified": "2023-01-01T00:00:00Z",
            "version": 'W/"1"',
        },
    }

    response: Response = make_response(
        jsonify(resource_type),
    )
    response.headers["Content-Type"] = "application/scim+json"
    return response
