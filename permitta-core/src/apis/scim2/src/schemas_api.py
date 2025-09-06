from app_logger import Logger, get_logger
from flask import Blueprint, jsonify, make_response, request, Response
from .schemas import user_schema, group_schema

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
        "Resources": [user_schema, group_schema],
    }

    response: Response = make_response(
        jsonify(schemas),
    )
    response.headers["Content-Type"] = "application/scim+json"
    return response
