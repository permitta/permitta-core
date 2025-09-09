from app_logger import Logger, get_logger
from flask import Blueprint, jsonify, make_response, request, Response

logger: Logger = get_logger("scim2.resource_type_group_api")
bp = Blueprint(
    "scim2_resource_type_group", __name__, url_prefix="/api/scim/v2/ResourceTypes/Group"
)


@bp.route("", methods=["GET"])
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