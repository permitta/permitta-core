import gzip
import json

from app_logger import Logger, get_logger

logger: Logger = get_logger("opa.decision_log_api")

from flask import Blueprint, g, request
from repositories import DecisionLogRepository

bp = Blueprint("opa_decision", __name__, url_prefix="/v1/opa/decision")


@bp.route("", methods=["POST"])
def create():
    body = gzip.decompress(request.data)
    logger.info(f"request: {body}")
    decision_logs: list[dict] = json.loads(body.decode("utf-8"))
    with g.database.Session.begin() as session:
        DecisionLogRepository.create_bulk(session=session, decision_logs=decision_logs)
        session.commit()

    return "ok"
