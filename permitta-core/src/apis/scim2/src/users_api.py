from app_logger import Logger, get_logger
from flask import Blueprint, jsonify, make_response, request, Response, g
import uuid
from repositories import PrincipalRepository
from models import PrincipalDbo
from api_services import ScimUsersService

logger: Logger = get_logger("scim2.users_api")
bp = Blueprint("scim2_users", __name__, url_prefix="/api/scim/v2/Users")


def create_user_id() -> str:
    return str(uuid.uuid4())


@bp.route("", methods=["GET"])
def get_users():
    # TODO add pagination support
    with g.database.Session.begin() as session:
        repo = PrincipalRepository()
        count, principals = repo.get_all_by_source(session=session, source_type="scim")

        users = {
            "schemas": ["urn:ietf:params:scim:api:messages:2.0:ListResponse"],
            "totalResults": count,
            "Resources": [principal.scim_payload for principal in principals],
        }

        response: Response = make_response(
            jsonify(users),
        )
    response.headers["Content-Type"] = "application/scim+json"
    return response


@bp.route("/<user_id>", methods=["GET"])
def get_user(user_id):
    with g.database.Session.begin() as session:
        principal = PrincipalRepository.get_by_source_uid(
            session=session, source_uid=user_id
        )
        if not principal:
            response: Response = make_response(
                jsonify(
                    {
                        "schemas": ["urn:ietf:params:scim:api:messages:2.0:Error"],
                        "detail": f"User with ID {user_id} not found",
                        "status": 404,
                    }
                ),
            )
            response.status_code = 404

        else:
            response: Response = make_response(
                jsonify(principal.scim_payload),
            )
    response.headers["Content-Type"] = "application/scim+json"
    return response


@bp.route("", methods=["POST"])
def create_user():
    scim_payload = request.json
    source_uid = scim_payload.get(
        "id", create_user_id()
    )  # respect the source ID if present or create a new one
    scim_payload = scim_payload | {"id": source_uid}

    with g.database.Session.begin() as session:
        scim_payload: dict = ScimUsersService().create_user(
            session=session, scim_payload=scim_payload
        )
        session.commit()
        response: Response = make_response(jsonify(scim_payload), 201)
    response.headers["Content-Type"] = "application/scim+json"
    return response


@bp.route("/<user_id>", methods=["PUT"])
def update_user(user_id):
    scim_payload = request.json
    source_uid = user_id

    with g.database.Session.begin() as session:
        principal: PrincipalDbo = PrincipalRepository.get_by_source_uid(
            session=session, source_uid=source_uid
        )
        ScimUsersService.update_user(
            session=session,
            scim_payload=scim_payload,
            principal=principal,
        )
        session.commit()

        response: Response = make_response(
            jsonify(scim_payload), 200
        )  # Created status code
    response.headers["Content-Type"] = "application/scim+json"
    return response


@bp.route("/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    source_uid = user_id
    with g.database.Session.begin() as session:
        principal: PrincipalDbo = PrincipalRepository.get_by_source_uid(
            session=session, source_uid=source_uid
        )
        if not principal:
            response: Response = make_response(
                jsonify(
                    {
                        "schemas": ["urn:ietf:params:scim:api:messages:2.0:Error"],
                        "detail": f"User with ID {user_id} not found",
                        "status": 404,
                    }
                ),
            )
            response.status_code = 404
        else:
            session.delete(principal)
            session.commit()
            response: Response = make_response()
            response.status_code = 204

    response.headers["Content-Type"] = "application/scim+json"
    return response
