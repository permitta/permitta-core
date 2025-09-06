import pytest
from flask import Flask
from app import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_service_provider_config(client):
    """Test the /ServiceProviderConfig endpoint."""
    response = client.get("/ServiceProviderConfig")
    assert response.status_code == 200
    data = response.get_json()
    assert "schemas" in data
    assert "urn:ietf:params:scim:schemas:core:2.0:ServiceProviderConfig" in data["schemas"]

def test_resource_types(client):
    """Test the /ResourceTypes endpoint."""
    response = client.get("/ResourceTypes")
    assert response.status_code == 200
    data = response.get_json()
    assert "schemas" in data
    assert "urn:ietf:params:scim:api:messages:2.0:ListResponse" in data["schemas"]
    assert "Resources" in data
    assert len(data["Resources"]) > 0
    assert data["Resources"][0]["id"] == "User"

def test_schemas(client):
    """Test the /Schemas endpoint."""
    response = client.get("/Schemas")
    assert response.status_code == 200
    data = response.get_json()
    assert "schemas" in data
    assert "urn:ietf:params:scim:api:messages:2.0:ListResponse" in data["schemas"]
    assert "Resources" in data
    assert len(data["Resources"]) > 0
    assert data["Resources"][0]["id"] == "urn:ietf:params:scim:schemas:core:2.0:User"

def test_resource_type_user(client):
    """Test the /ResourceType/User endpoint."""
    response = client.get("/ResourceType/User")
    assert response.status_code == 200
    data = response.get_json()
    assert "schemas" in data
    assert "urn:ietf:params:scim:schemas:core:2.0:ResourceType" in data["schemas"]
    assert data["id"] == "User"

def test_schemas_user(client):
    """Test the /Schemas/urn:ietf:params:scim:schemas:core:2.0:User endpoint."""
    response = client.get("/Schemas/urn:ietf:params:scim:schemas:core:2.0:User")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == "urn:ietf:params:scim:schemas:core:2.0:User"
    assert "attributes" in data
    assert len(data["attributes"]) > 0