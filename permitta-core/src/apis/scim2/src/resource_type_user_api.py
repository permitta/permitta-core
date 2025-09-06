from app_logger import Logger, get_logger
from flask import Blueprint, jsonify, make_response, request, Response

logger: Logger = get_logger("scim2.resource_type_user_api")
bp = Blueprint(
    "scim2_resource_type_user", __name__, url_prefix="/api/scim/v2/ResourceTypes/User"
)


@bp.route("", methods=["GET"])
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
