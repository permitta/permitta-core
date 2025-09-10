from flask import request, jsonify, abort
from app_logger import Logger, get_logger
from apis.models import ApiConfig

logger: Logger = get_logger("authenticator")


def authenticate(api_config: ApiConfig):
    def no_auth_decorator(func):
        def wrapper(*args, **kwargs):
            logger.info(f"Processed api call without authentication")
            return func(*args, **kwargs)

        wrapper.__name__ = func.__name__
        return wrapper

    def api_key_auth_decorator(func):
        def wrapper(*args, **kwargs):
            if request.headers.get("Authorization") == f"Bearer {api_config.api_key}":
                return func(*args, **kwargs)

            logger.info(f"Unauthorized request from {request.remote_addr}")
            abort(401, description="Authentication failed")

        wrapper.__name__ = func.__name__
        return wrapper

    def oauth2_auth_decorator(func):
        def wrapper(*args, **kwargs):
            raise NotImplementedError

    if api_config.auth_method == "none":
        return no_auth_decorator
    if api_config.auth_method == "api-key":
        return api_key_auth_decorator
    if api_config.auth_method == "oauth2":
        return oauth2_auth_decorator
    else:
        raise ValueError(f"Invalid auth method: {api_config.auth_method}")
