import pytest
from unittest.mock import patch
from flask import Flask, jsonify
from arctic_office_projects_api import auth_required


@pytest.fixture
def app():
    app = Flask(__name__)

    @app.route("/protected")
    @auth_required()
    def protected():
        return jsonify({"message": "Success"}), 200

    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_missing_authorization_header(client):
    response = client.get("/protected")
    assert response.status_code == 401
    data = response.get_json()
    assert data["error"] == "Missing or invalid Authorization header"


def test_invalid_authorization_header(client):
    response = client.get("/protected", headers={"Authorization": "NotBearer token"})
    assert response.status_code == 401
    data = response.get_json()
    assert data["error"] == "Missing or invalid Authorization header"


def test_validate_token_failure(client):
    with patch("arctic_office_projects_api.validate_token", side_effect=Exception("Bad token")):
        response = client.get("/protected", headers={"Authorization": "Bearer fake_token"})
        assert response.status_code == 401
        data = response.get_json()
        assert data["error"] == "Invalid token"
        assert "Bad token" in data["detail"]


def test_validate_token_success(client):
    with patch("arctic_office_projects_api.validate_token", return_value={"sub": "test-user"}):
        response = client.get("/protected", headers={"Authorization": "Bearer fake_token"})
        assert response.status_code == 200
        data = response.get_json()
        assert data["message"] == "Success"
