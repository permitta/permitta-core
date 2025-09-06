from app_logger import Logger, get_logger
from flask import Blueprint, jsonify, make_response, request, Response
from .schemas import group_schema

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
    response: Response = make_response(
        jsonify(group_schema),
    )
    response.headers["Content-Type"] = "application/scim+json"
    return response
