import json
from flask.testing import FlaskClient
from unittest.mock import patch

from database import Database
from models import PrincipalDbo


def test_create_user(flask_test_client: FlaskClient, database_empty: Database):
    """
    A post to this endpoint should create a new user in the database.
    If this username already exists, the endpoint should return a 409 error.
    The source_type should be set to "scim" and the source_uid should be set to a UUID.
    The response should contain the same content which was sent in, plus the id field
    """

    user_data = {
        "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
        "userName": "alice.cooper",
        "name": {"givenName": "Alice", "familyName": "Cooper"},
        "emails": [
            {"value": "alice.cooper@moat.io", "primary": True},
            {"value": "alice.cooper@hotmail.com"},
        ],
        "active": True,
    }

    with patch(
        "apis.scim2.src.users_api.create_id",
        return_value="12345678-1234-5678-1234-567812345678",
    ):
        response = flask_test_client.post(
            "/api/scim/v2/Users",
            data=json.dumps(user_data),
            content_type="application/json",
        )

        assert response.status_code == 201
        assert response.headers["Content-Type"] == "application/scim+json"
        response_payload: dict = response.get_json()

        # we should get the same content back with the user id
        assert response_payload == user_data | {
            "id": "12345678-1234-5678-1234-567812345678"
        }

        with database_empty.Session.begin() as session:
            principal: PrincipalDbo | None = (
                session.query(PrincipalDbo)
                .filter(
                    PrincipalDbo.source_uid == "12345678-1234-5678-1234-567812345678"
                )
                .first()
            )
            assert principal is not None

            assert principal.fq_name == "alice.cooper"
            assert principal.first_name == "Alice"
            assert principal.last_name == "Cooper"
            assert principal.user_name == "alice.cooper"
            assert principal.email == "alice.cooper@moat.io"
            assert principal.source_uid == "12345678-1234-5678-1234-567812345678"
            assert principal.source_type == "scim"
            assert principal.scim_payload == user_data | {
                "id": "12345678-1234-5678-1234-567812345678"
            }


def test_create_user_with_confliction(
    flask_test_client: FlaskClient, database_empty: Database
):
    with patch(
        "apis.scim2.src.users_api.create_id",
        return_value="12345678-1234-5678-1234-567812345678",
    ):
        response = flask_test_client.post(
            "/api/scim/v2/Users",
            data=json.dumps({}),
            content_type="application/json",
        )
        assert response.status_code == 409
        assert response.headers["Content-Type"] == "application/scim+json"
        assert response.json == {
            "schemas": ["urn:ietf:params:scim:api:messages:2.0:Error"],
            "detail": "User with ID 12345678-1234-5678-1234-567812345678 already exists",
            "status": 409,
        }


def test_get_users(flask_test_client: FlaskClient):
    response = flask_test_client.get(f"/api/scim/v2/Users")

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/scim+json"

    assert response.json == {
        "schemas": ["urn:ietf:params:scim:api:messages:2.0:ListResponse"],
        "totalResults": 1,
        "startIndex": 1,
        "itemsPerPage": 10000,
        "Resources": [
            {
                "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
                "id": "12345678-1234-5678-1234-567812345678",
                "userName": "alice.cooper",
                "name": {"givenName": "Alice", "familyName": "Cooper"},
                "emails": [
                    {"value": "alice.cooper@moat.io", "primary": True},
                    {"value": "alice.cooper@hotmail.com"},
                ],
                "active": True,
            }
        ],
    }


def test_get_user(flask_test_client: FlaskClient):
    user_id: str = "12345678-1234-5678-1234-567812345678"
    response = flask_test_client.get(f"/api/scim/v2/Users/{user_id}")

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/scim+json"
    assert response.json == {
        "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
        "id": "12345678-1234-5678-1234-567812345678",
        "userName": "alice.cooper",
        "name": {"givenName": "Alice", "familyName": "Cooper"},
        "emails": [
            {"value": "alice.cooper@moat.io", "primary": True},
            {"value": "alice.cooper@hotmail.com"},
        ],
        "active": True,
    }


def test_get_user_not_found(flask_test_client: FlaskClient):
    user_id: str = "c0835e00-1859-4927-8293-e2fd064fda0a"
    response = flask_test_client.get(f"/api/scim/v2/Users/{user_id}")

    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/scim+json"
    assert response.json == {
        "schemas": ["urn:ietf:params:scim:api:messages:2.0:Error"],
        "detail": f"User with ID c0835e00-1859-4927-8293-e2fd064fda0a not found",
        "status": 404,
    }


def test_update_user(flask_test_client: FlaskClient, database_empty: Database):
    user_id: str = "12345678-1234-5678-1234-567812345678"
    response = flask_test_client.get(f"/api/scim/v2/Users/{user_id}")
    assert response.status_code == 200

    # change the user data and PUT it back
    user_data = {
        "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
        "id": "12345678-1234-5678-1234-567812345678",
        "userName": "boris.yeltsin",
        "name": {"givenName": "Boris", "familyName": "Yeltsin"},
        "emails": [{"value": "boris.yeltsin@moat.io", "primary": True}],
        "active": False,
    }

    response = flask_test_client.put(
        f"/api/scim/v2/Users/{user_id}",
        data=json.dumps(user_data),
        content_type="application/json",
    )

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/scim+json"
    assert response.json == user_data

    with database_empty.Session.begin() as session:
        principal: PrincipalDbo | None = (
            session.query(PrincipalDbo)
            .filter(PrincipalDbo.source_uid == "12345678-1234-5678-1234-567812345678")
            .first()
        )
        assert principal is not None

        assert principal.fq_name == "boris.yeltsin"
        assert principal.first_name == "Boris"
        assert principal.last_name == "Yeltsin"
        assert principal.user_name == "boris.yeltsin"
        assert principal.email == "boris.yeltsin@moat.io"
        assert principal.source_uid == "12345678-1234-5678-1234-567812345678"
        assert principal.source_type == "scim"
        assert principal.scim_payload == user_data


def test_update_user_not_found(flask_test_client: FlaskClient):
    user_id: str = "c0835e00-1859-4927-8293-e2fd064fda0a"
    response = flask_test_client.put(
        f"/api/scim/v2/Users/{user_id}",
        data=json.dumps({}),
        content_type="application/json",
    )

    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/scim+json"
    assert response.json == {
        "schemas": ["urn:ietf:params:scim:api:messages:2.0:Error"],
        "detail": f"User with ID c0835e00-1859-4927-8293-e2fd064fda0a not found",
        "status": 404,
    }


def test_delete_user(flask_test_client: FlaskClient):
    user_id: str = "12345678-1234-5678-1234-567812345678"
    response = flask_test_client.delete(f"/api/scim/v2/Users/{user_id}")

    assert response.status_code == 204
    assert response.headers["Content-Type"] == "application/scim+json"


def test_delete_user_not_found(flask_test_client: FlaskClient):
    user_id: str = "c0835e00-1859-4927-8293-e2fd064fda0a"
    response = flask_test_client.delete(f"/api/scim/v2/Users/{user_id}")

    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/scim+json"
    assert response.json == {
        "schemas": ["urn:ietf:params:scim:api:messages:2.0:Error"],
        "detail": f"User with ID c0835e00-1859-4927-8293-e2fd064fda0a not found",
        "status": 404,
    }
