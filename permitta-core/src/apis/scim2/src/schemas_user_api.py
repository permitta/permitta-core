from app_logger import Logger, get_logger
from flask import Blueprint, jsonify, make_response, request, Response
from .schemas import user_schema

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
    response: Response = make_response(
        jsonify(user_schema),
    )
    response.headers["Content-Type"] = "application/scim+json"
    return response
