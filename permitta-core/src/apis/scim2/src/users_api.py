from app_logger import Logger, get_logger
from flask import Blueprint, jsonify, make_response, request, Response, g
import uuid
from repositories import PrincipalRepository
from models import PrincipalDbo

logger: Logger = get_logger("scim2.users_api")
bp = Blueprint("scim2_users", __name__, url_prefix="/api/scim/v2/Users")


@bp.route("", methods=["GET"])
def get_users():
    """
    Get Users.

    This endpoint returns a list of Users.
    """
    with g.database.Session.begin() as session:
        repo = PrincipalRepository()
        count, principals = repo.get_all(session=session)

        users = {
            "schemas": ["urn:ietf:params:scim:api:messages:2.0:ListResponse"],
            "totalResults": count,
            "Resources": [principal.scim_payload for principal in principals],
        }

        # users = {
        #     "schemas": ["urn:ietf:params:scim:api:messages:2.0:ListResponse"],
        #     "totalResults": 1,
        #     "Resources": [
        #         {
        #             "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
        #             "id": "2819c223-7f76-453a-919d-413861904646",
        #             "userName": "bjensen@example.com",
        #             "name": {
        #                 "formatted": "Ms. Barbara J Jensen, III",
        #                 "familyName": "Jensen",
        #                 "givenName": "Barbara",
        #             },
        #             "emails": [
        #                 {"value": "bjensen@example.com", "type": "work", "primary": True}
        #             ],
        #             "active": True,
        #             "meta": {
        #                 "resourceType": "User",
        #                 "created": "2023-01-01T00:00:00Z",
        #                 "lastModified": "2023-01-01T00:00:00Z",
        #                 "location": "/Users/2819c223-7f76-453a-919d-413861904646",
        #                 "version": 'W/"1"',
        #             },
        #         }
        #     ],
        # }

        response: Response = make_response(
            jsonify(users),
        )
    response.headers["Content-Type"] = "application/scim+json"
    return response


@bp.route("/<user_id>", methods=["GET"])
def get_user(user_id):
    """
    Get a User by ID.

    This endpoint returns a specific User by ID.
    """
    with g.database.Session.begin() as session:
        principal = PrincipalRepository.get_by_source_uid(
            session=session, source_uid=user_id
        )
        if not principal:
            return make_response(
                jsonify(
                    {
                        "schemas": ["urn:ietf:params:scim:api:messages:2.0:Error"],
                        "detail": f"User with ID {user_id} not found",
                        "status": 404,
                    }
                ),
            )

        response: Response = make_response(
            jsonify(principal.scim_payload),
        )
    response.headers["Content-Type"] = "application/scim+json"
    return response


@bp.route("", methods=["POST"])
def create_user():
    """
    Create a User.

    This endpoint creates a new User.
    """
    user_data = request.json
    source_uid = str(uuid.uuid4())
    scim_payload = user_data | {"id": source_uid}

    with g.database.Session.begin() as session:
        principal: PrincipalDbo = PrincipalDbo()
        principal.fq_name = user_data.get("userName", "")
        principal.first_name = user_data.get("name", {}).get("givenName", "")
        principal.last_name = user_data.get("name", {}).get("familyName", "")
        principal.email = user_data.get("emails", [{}])[0].get("value", "")
        principal.source_uid = user_data.get("id", "")
        principal.source_type = "scim"
        principal.source_uid = source_uid
        principal.scim_payload = scim_payload
        session.add(principal)
        session.commit()

        response: Response = make_response(
            jsonify(scim_payload), 201
        )  # Created status code
    response.headers["Content-Type"] = "application/scim+json"
    return response


@bp.route("/<user_id>", methods=["PUT"])
def update_user(user_id):
    user_data = request.json
    source_uid = user_id
    scim_payload = user_data | {"id": source_uid}

    with g.database.Session.begin() as session:
        principal: PrincipalDbo = PrincipalRepository.get_by_source_uid(
            session=session, source_uid=source_uid
        )
        principal.fq_name = user_data.get("userName", "")
        principal.first_name = user_data.get("name", {}).get("givenName", "")
        principal.last_name = user_data.get("name", {}).get("familyName", "")
        principal.email = user_data.get("emails", [{}])[0].get("value", "")
        principal.source_uid = user_data.get("id", "")
        principal.source_type = "scim"
        principal.source_uid = source_uid
        principal.scim_payload = scim_payload
        session.add(principal)
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
            return make_response(
                jsonify(
                    {
                        "schemas": ["urn:ietf:params:scim:api:messages:2.0:Error"],
                        "detail": f"User with ID {user_id} not found",
                        "status": 404,
                    }
                ),
            )
        session.delete(principal)
        session.commit()

    response: Response = make_response()
    response.status_code = 204
    response.headers["Content-Type"] = "application/scim+json"
    return response
