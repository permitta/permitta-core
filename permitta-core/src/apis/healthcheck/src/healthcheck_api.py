from app_logger import Logger, get_logger
from flask import Blueprint, Response, g, jsonify, make_response, request
from app_config import AppConfigModelBase
from auth import require_api_key

logger: Logger = get_logger("api.healthcheck")

bp = Blueprint("healthcheck_api_v1", __name__, url_prefix="/api/v1/healthcheck")


class ApiHealthCheckConfig(AppConfigModelBase):
    CONFIG_PREFIX: str = "api.healthcheck"
    api_key: str = None


api_healthcheck_config: ApiHealthCheckConfig = ApiHealthCheckConfig.load()


@bp.route("/", methods=["GET"])
@require_api_key(api_key=api_healthcheck_config.api_key)
def index():
    response: Response = make_response(jsonify({"status": "ok"}))
    return response
