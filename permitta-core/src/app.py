from datetime import datetime, timezone

from apis.data_objects import data_objects_api_bp
from apis.opa import bundle_api_bp, decision_log_api_bp, status_api_bp
from apis.healthcheck import healthcheck_bp
from apis.scim2 import (
    scim2_service_provider_config_bp,
    scim2_resource_types_bp,
    scim2_schemas_bp,
    scim2_resource_type_user_bp,
    scim2_users_bp,
    scim2_resource_type_group_bp,
    scim2_groups_bp,
)
from app_config import AppConfigModelBase
from app_logger import Logger, get_logger
from auth import OpaAuthzProvider
from database import Database
from flask import Flask, g, request, jsonify
from werkzeug.exceptions import HTTPException

logger: Logger = get_logger("app")


class FlaskConfig(AppConfigModelBase):
    CONFIG_PREFIX: str = "flask"
    secret_key: str = None
    static_url_path: str = ""
    static_folder: str = "../ui/static"
    template_folder: str = "../ui/templates"


def create_app(database: Database | None = None) -> Flask:
    flask_config = FlaskConfig.load()

    flask_app = Flask(
        __name__,
        static_url_path=flask_config.static_url_path,
        static_folder=flask_config.static_folder,
        template_folder=flask_config.template_folder,
    )
    flask_app.secret_key = flask_config.secret_key

    # Database
    database: Database = Database()
    database.connect()

    # enable APIs
    flask_app.register_blueprint(bundle_api_bp)
    flask_app.register_blueprint(decision_log_api_bp)
    flask_app.register_blueprint(status_api_bp)
    flask_app.register_blueprint(data_objects_api_bp)
    flask_app.register_blueprint(healthcheck_bp)

    # Register SCIM2 blueprints
    flask_app.register_blueprint(scim2_service_provider_config_bp)
    flask_app.register_blueprint(scim2_resource_types_bp)
    flask_app.register_blueprint(scim2_schemas_bp)
    flask_app.register_blueprint(scim2_resource_type_user_bp)
    flask_app.register_blueprint(scim2_users_bp)
    flask_app.register_blueprint(scim2_resource_type_group_bp)
    flask_app.register_blueprint(scim2_groups_bp)

    @flask_app.errorhandler(HTTPException)
    def handle_exception(e):
        if request.path.startswith(
            "/api/scim/"
        ):  # Check if the request is for the SCIM API
            response = jsonify(
                {
                    "schemas": ["urn:ietf:params:scim:api:messages:2.0:Error"],
                    "detail": e.description,
                    "status": f"{e.code}",
                }
            )
            response.status_code = e.code
            return response
        else:
            return e  # return all others to flask

    @flask_app.before_request
    def before_request():
        # connect DB
        g.database = database

    @flask_app.after_request
    def after_request(response):
        timestamp = datetime.now(tz=timezone.utc).strftime("[%Y-%b-%d %H:%M]")
        logger.info(
            "%s %s %s %s %s %s",
            timestamp,
            request.remote_addr,
            request.method,
            request.scheme,
            request.full_path,
            response.status,
        )
        return response

    return flask_app
