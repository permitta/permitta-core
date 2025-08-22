from app_logger import Logger, get_logger
from flask import Blueprint

bp = Blueprint("opa_status", __name__, url_prefix="/v1/opa/status")
logger: Logger = get_logger("opa.status_api")


@bp.route("", methods=["POST"])
# @validate()
def post() -> str:
    # logger.info(f"Received status update from OPA: {request.json}")
    return "ok"
