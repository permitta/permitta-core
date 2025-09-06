from app_logger import Logger, get_logger
from flask import Blueprint, jsonify, make_response, request, Response

logger: Logger = get_logger("scim2.service_provider_config_api")
bp = Blueprint(
    "scim2_service_provider_config",
    __name__,
    url_prefix="/api/scim/v2/ServiceProviderConfig",
)


@bp.route("", methods=["GET"])
def get_service_provider_config():
    """
    Get the Service Provider Configuration.

    This endpoint returns information about the SCIM service provider's configuration.
    """
    service_provider_config = {
        "schemas": ["urn:ietf:params:scim:schemas:core:2.0:ServiceProviderConfig"],
        "documentationUri": "http://example.com/documentation",
        "patch": {"supported": False},
        "bulk": {"supported": False, "maxOperations": 0, "maxPayloadSize": 0},
        "filter": {"supported": True, "maxResults": 100},
        "changePassword": {"supported": False},
        "sort": {"supported": True},
        "etag": {"supported": False},
        "authenticationSchemes": [
            {
                "name": "OAuth Bearer Token",
                "description": "Authentication scheme using the OAuth Bearer Token Standard",
                "specUri": "http://www.rfc-editor.org/info/rfc6750",
                "documentationUri": "http://example.com/documentation/oauth",
                "type": "oauthbearertoken",
                "primary": True,
            }
        ],
        "meta": {
            "location": "/ServiceProviderConfig",
            "resourceType": "ServiceProviderConfig",
            "created": "2023-01-01T00:00:00Z",
            "lastModified": "2023-01-01T00:00:00Z",
            "version": 'W/"1"',
        },
    }

    response: Response = make_response(
        jsonify(service_provider_config),
    )
    response.headers["Content-Type"] = "application/scim+json"
    return response
