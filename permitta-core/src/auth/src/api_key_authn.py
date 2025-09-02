from flask import request, jsonify


def require_api_key(api_key: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if request.headers.get("Authorization") == f"Bearer {api_key}":
                return func(*args, **kwargs)
            return jsonify({"status": "unauthorized"}), 401

        return wrapper

    return decorator
