from dataclasses import asdict

from app_logger import Logger, get_logger
from flask import Blueprint, Response, g, jsonify, make_response

logger: Logger = get_logger("api.healthcheck")

bp = Blueprint("healthcheck_api_v1", __name__, url_prefix="/api/v1/healthcheck")


@bp.route("/", methods=["GET"])
def index():
    response: Response = make_response(jsonify({"status": "ok"}))
    return response
