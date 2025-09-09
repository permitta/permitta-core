import json
from flask.testing import FlaskClient
from unittest.mock import patch

from database import Database
from models import PrincipalDbo


def test_get_users_with_pagination_empty(flask_test_client: FlaskClient):
    response = flask_test_client.get(f"/api/scim/v2/Users?startIndex=1&count=2")

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/scim+json"

    assert response.json == {
        "schemas": ["urn:ietf:params:scim:api:messages:2.0:ListResponse"],
        "totalResults": 0,
        "startIndex": 1,
        "itemsPerPage": 2,
        "Resources": [],
    }


def test_get_users_with_pagination(flask_test_client: FlaskClient):
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

    for i in range(0, 10):
        flask_test_client.post(
            "/api/scim/v2/Users",
            data=json.dumps(user_data),
            content_type="application/json",
        )

    response = flask_test_client.get("/api/scim/v2/Users?startIndex=1&count=2")

    assert response.json["totalResults"] == 10
    assert response.json["startIndex"] == 1
    assert response.json["itemsPerPage"] == 2
    assert len(response.json["Resources"]) == 2

    response = flask_test_client.get("/api/scim/v2/Users?startIndex=3&count=5")

    assert response.json["totalResults"] == 10
    assert response.json["startIndex"] == 3
    assert response.json["itemsPerPage"] == 5
    assert len(response.json["Resources"]) == 5

    response = flask_test_client.get("/api/scim/v2/Users?startIndex=8&count=5")

    assert response.json["totalResults"] == 10
    assert response.json["startIndex"] == 8
    assert response.json["itemsPerPage"] == 5
    assert len(response.json["Resources"]) == 3
