from app_logger import Logger, get_logger
from flask import Blueprint, jsonify, make_response, request, Response, g
import uuid
from repositories import PrincipalRepository
from models import PrincipalDbo

logger: Logger = get_logger("scim2.groups_api")
bp = Blueprint("scim2_groups", __name__, url_prefix="/api/scim/v2/Groups")


@bp.route("", methods=["GET"])
def get_groups():
    """
    Get Groups.

    This endpoint returns a list of Groups.
    """
    with g.database.Session.begin() as session:
        repo = PrincipalRepository()
        count, principals = repo.get_all(session=session)
        
        # Filter principals to only include those that are groups
        group_principals = [p for p in principals if p.scim_payload.get("schemas") == ["urn:ietf:params:scim:schemas:core:2.0:Group"]]
        group_count = len(group_principals)

        groups = {
            "schemas": ["urn:ietf:params:scim:api:messages:2.0:ListResponse"],
            "totalResults": group_count,
            "Resources": [principal.scim_payload for principal in group_principals],
        }

        response: Response = make_response(
            jsonify(groups),
        )
    response.headers["Content-Type"] = "application/scim+json"
    return response


@bp.route("/<group_id>", methods=["GET"])
def get_group(group_id):
    """
    Get a Group by ID.

    This endpoint returns a specific Group by ID.
    """
    with g.database.Session.begin() as session:
        principal = PrincipalRepository.get_by_source_uid(
            session=session, source_uid=group_id
        )
        if not principal or principal.scim_payload.get("schemas") != ["urn:ietf:params:scim:schemas:core:2.0:Group"]:
            return make_response(
                jsonify(
                    {
                        "schemas": ["urn:ietf:params:scim:api:messages:2.0:Error"],
                        "detail": f"Group with ID {group_id} not found",
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
def create_group():
    """
    Create a Group.

    This endpoint creates a new Group.
    """
    group_data = request.json
    source_uid = str(uuid.uuid4())
    scim_payload = group_data | {"id": source_uid}

    with g.database.Session.begin() as session:
        principal: PrincipalDbo = PrincipalDbo()
        principal.fq_name = group_data.get("displayName", "")
        principal.source_uid = source_uid
        principal.source_type = "scim"
        principal.scim_payload = scim_payload
        session.add(principal)
        session.commit()

        response: Response = make_response(
            jsonify(scim_payload), 201
        )  # Created status code
    response.headers["Content-Type"] = "application/scim+json"
    return response


@bp.route("/<group_id>", methods=["PUT"])
def update_group(group_id):
    """
    Update a Group.

    This endpoint updates an existing Group.
    """
    group_data = request.json
    source_uid = group_id
    scim_payload = group_data | {"id": source_uid}

    with g.database.Session.begin() as session:
        principal: PrincipalDbo = PrincipalRepository.get_by_source_uid(
            session=session, source_uid=source_uid
        )
        if not principal or principal.scim_payload.get("schemas") != ["urn:ietf:params:scim:schemas:core:2.0:Group"]:
            return make_response(
                jsonify(
                    {
                        "schemas": ["urn:ietf:params:scim:api:messages:2.0:Error"],
                        "detail": f"Group with ID {group_id} not found",
                        "status": 404,
                    }
                ),
            )
        
        principal.fq_name = group_data.get("displayName", "")
        principal.source_uid = source_uid
        principal.source_type = "scim"
        principal.scim_payload = scim_payload
        session.add(principal)
        session.commit()

        response: Response = make_response(
            jsonify(scim_payload), 200
        )
    response.headers["Content-Type"] = "application/scim+json"
    return response


@bp.route("/<group_id>", methods=["DELETE"])
def delete_group(group_id):
    """
    Delete a Group.

    This endpoint deletes a Group.
    """
    source_uid = group_id
    with g.database.Session.begin() as session:
        principal: PrincipalDbo = PrincipalRepository.get_by_source_uid(
            session=session, source_uid=source_uid
        )
        if not principal or principal.scim_payload.get("schemas") != ["urn:ietf:params:scim:schemas:core:2.0:Group"]:
            return make_response(
                jsonify(
                    {
                        "schemas": ["urn:ietf:params:scim:api:messages:2.0:Error"],
                        "detail": f"Group with ID {group_id} not found",
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