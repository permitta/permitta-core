from flask.testing import FlaskClient


def test_index(flask_test_client: FlaskClient):
    response = flask_test_client.get("/api/v1/healthcheck")
    assert response.status_code == 200
    assert response.json == {"status": "ok"}
