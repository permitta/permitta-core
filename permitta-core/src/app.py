from datetime import datetime, timezone

from apis.data_objects import data_objects_api_bp
from apis.opa import bundle_api_bp, decision_log_api_bp, status_api_bp
from app_config import AppConfigModelBase
from app_logger import Logger, get_logger
from auth import OpaAuthzProvider
from database import Database
from flask import Flask, g, request

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

    # AuthZ - set the policy doc on OPA at startup
    authz: OpaAuthzProvider = OpaAuthzProvider(user_name="app", user_attributes=[])
    authz.apply_policy_to_opa()

    # enable APIs
    flask_app.register_blueprint(bundle_api_bp)
    flask_app.register_blueprint(decision_log_api_bp)
    flask_app.register_blueprint(status_api_bp)
    flask_app.register_blueprint(data_objects_api_bp)

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
