from app_logger import Logger, get_logger
from flask import send_from_directory
from flask_pydantic import validate

logger: Logger = get_logger("opa.bundle_api")

from flask import Blueprint, g

from opa import BundleGenerator

bp = Blueprint("opa_bundle", __name__, url_prefix="/v1/opa/bundle")


@bp.route("/<platform>", methods=["GET"])
@validate()
def get_bundle(platform: str):
    with g.database.Session.begin() as session:
        with BundleGenerator(
            session=session, platform=platform, bundle_name="trino"
        ) as bundle:
            return send_from_directory(
                directory=bundle.directory,
                path=bundle.filename,
                mimetype="application/octet-stream",
            )
