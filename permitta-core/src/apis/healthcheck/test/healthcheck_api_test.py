from flask.testing import FlaskClient


def test_index(flask_test_client: FlaskClient):
    # no auth
    response = flask_test_client.get("/api/v1/healthcheck/")
    assert response.status_code == 401

    # bad auth
    response = flask_test_client.get(
        "/api/v1/healthcheck/",
        headers={"Authorization": "Bearer a-secret-api-key-which-is-bad"},
    )
    assert response.status_code == 401
    assert response.json == {"status": "unauthorized"}

    # good auth
    response = flask_test_client.get(
        "/api/v1/healthcheck/", headers={"Authorization": "Bearer a-secret-api-key"}
    )
    assert response.status_code == 200
    assert response.json == {"status": "ok"}
