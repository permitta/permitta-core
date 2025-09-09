import json
from flask.testing import FlaskClient
from unittest.mock import patch
from typing import Tuple
from database import Database
from models import PrincipalDbo
from urllib.parse import quote


def assert_attributes_match(
    principal: PrincipalDbo,
    expected_attributes: list[Tuple[str, str]],
):
    actual_attributes: list[Tuple[str, str]] = [
        (a.attribute_key, a.attribute_value) for a in principal.attributes
    ]
    assert actual_attributes == expected_attributes


def test_create_user(flask_test_client: FlaskClient, database_empty: Database):
    """
    A post to this endpoint should create a new user in the database.
    If this username already exists, the endpoint should return a 409 error.
    The source_type should be set to "scim" and the source_uid should be set to a UUID.
    The response should contain the same content which was sent in, plus the id field
    """

    user_data = {
        "schemas": [
            "urn:ietf:params:scim:schemas:core:2.0:User",
            "urn:ietf:params:scim:schemas:extension:enterprise:2.0:User",
            "urn:ietf:params:scim:custom",
        ],
        "id": "alice.cooper@moat.io",  # has a pre-defined ID :/
        "userName": "alice.cooper",
        "name": {"givenName": "Alice", "familyName": "Cooper"},
        "emails": [
            {"value": "alice.cooper@moat.io", "primary": True},
            {"value": "alice.cooper@hotmail.com"},
        ],
        "active": True,
        "urn:ietf:params:scim:schemas:extension:enterprise:2.0:User": {},
        "urn:ietf:params:scim:custom": {
            "Employee": "True",
            "Redact": "PII",
            "Domain": ["Sales", "Customer", "HR"],
        },
    }

    response = flask_test_client.post(
        "/api/scim/v2/Users",
        data=json.dumps(user_data),
        content_type="application/json",
        headers={"Authorization": "Bearer scim-token"},
    )

    assert response.status_code == 201
    assert response.headers["Content-Type"] == "application/scim+json"
    response_payload: dict = response.get_json()

    # we should get the same content back with the supplied user id
    assert response_payload == user_data

    with database_empty.Session.begin() as session:
        principal: PrincipalDbo | None = (
            session.query(PrincipalDbo)
            .filter(PrincipalDbo.source_uid == "alice.cooper@moat.io")
            .first()
        )
        assert principal is not None

        assert principal.fq_name == "alice.cooper"
        assert principal.first_name == "Alice"
        assert principal.last_name == "Cooper"
        assert principal.user_name == "alice.cooper"
        assert principal.email == "alice.cooper@moat.io"
        assert principal.source_uid == "alice.cooper@moat.io"
        assert principal.source_type == "scim"
        assert principal.scim_payload == user_data

        # custom schema items should map to attributes on the PrincipalDbo model
        assert_attributes_match(
            principal,
            [
                ("Employee", "True"),
                ("Redact", "PII"),
                ("Domain", "Sales,Customer,HR"),
            ],
        )


def _get_updated_attributes(
    client: FlaskClient, db: Database, user_data: dict
) -> list[Tuple[str, str]]:
    user_id: str = "alice.cooper@moat.io"
    response = client.put(
        f"/api/scim/v2/Users/{user_id}",
        data=json.dumps(user_data),
        content_type="application/json",
        headers={"Authorization": "Bearer scim-token"},
    )

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/scim+json"
    assert response.json == user_data

    with db.Session.begin() as session:
        principal: PrincipalDbo | None = (
            session.query(PrincipalDbo)
            .filter(PrincipalDbo.source_uid == "alice.cooper@moat.io")
            .first()
        )
        assert principal is not None
        actual_attributes: list[Tuple[str, str]] = [
            (a.attribute_key, a.attribute_value) for a in principal.attributes
        ]
    return actual_attributes


def _get_user_data(client: FlaskClient, user_id: str = "alice.cooper@moat.io") -> dict:
    response = client.get(
        f"/api/scim/v2/Users/{user_id}",
        headers={"Authorization": "Bearer scim-token"},
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/scim+json"
    return response.json


def test_update_user_add_attribute(
    flask_test_client: FlaskClient, database_empty: Database
):
    # add a new attribute to the user
    user_data = _get_user_data(flask_test_client)
    user_data["urn:ietf:params:scim:custom"]["Department"] = "Sales"

    assert _get_updated_attributes(flask_test_client, database_empty, user_data) == [
        ("Employee", "True"),
        ("Redact", "PII"),
        ("Domain", "Sales,Customer,HR"),
        ("Department", "Sales"),
    ]


def test_update_user_remove_scalar_attribute(
    flask_test_client: FlaskClient, database_empty: Database
):
    user_data = _get_user_data(flask_test_client)
    del user_data["urn:ietf:params:scim:custom"]["Redact"]

    assert _get_updated_attributes(flask_test_client, database_empty, user_data) == [
        ("Employee", "True"),
        ("Domain", "Sales,Customer,HR"),
        ("Department", "Sales"),
    ]


def test_update_user_change_scalar_attribute(
    flask_test_client: FlaskClient, database_empty: Database
):
    user_data = _get_user_data(flask_test_client)
    user_data["urn:ietf:params:scim:custom"]["Department"] = "Nonsense"

    assert _get_updated_attributes(flask_test_client, database_empty, user_data) == [
        ("Employee", "True"),
        ("Domain", "Sales,Customer,HR"),
        ("Department", "Nonsense"),
    ]


def test_update_user_remove_array_item_attribute(
    flask_test_client: FlaskClient, database_empty: Database
):
    user_data = _get_user_data(flask_test_client)
    user_data["urn:ietf:params:scim:custom"]["Domain"] = ["Sales", "Customer"]

    assert _get_updated_attributes(flask_test_client, database_empty, user_data) == [
        ("Employee", "True"),
        ("Department", "Nonsense"),
        ("Domain", "Sales,Customer"),
    ]


def test_update_user_change_array_attribute(
    flask_test_client: FlaskClient, database_empty: Database
):
    user_data = _get_user_data(flask_test_client)
    user_data["urn:ietf:params:scim:custom"]["Domain"] = ["Cows", "Customer"]

    assert _get_updated_attributes(flask_test_client, database_empty, user_data) == [
        ("Employee", "True"),
        ("Department", "Nonsense"),
        ("Domain", "Cows,Customer"),
    ]


def test_update_user_remove_array_attribute(
    flask_test_client: FlaskClient, database_empty: Database
):
    user_data = _get_user_data(flask_test_client)
    del user_data["urn:ietf:params:scim:custom"]["Domain"]

    assert _get_updated_attributes(flask_test_client, database_empty, user_data) == [
        ("Employee", "True"),
        ("Department", "Nonsense"),
    ]
