import pytest
from arctic_office_projects_api import create_app

# Fixture to set up the Flask application for testing
@pytest.fixture
def app():
    app = create_app('testing')  # 'testing' corresponds to the appropriate config
    app.config.update({
        "TESTING": True,  # Enable testing mode (disables error catching, etc.)
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # Use an in-memory database
    })

    with app.app_context():
        # Initialize the database or any other setup required
        # db.create_all() if using a real database in tests

        yield app  # Provide the app instance to tests

# Fixture to set up the test client to make requests to the app
@pytest.fixture
def client(app):
    return app.test_client()  # Return a test client instance

# Fixture for creating a test runner for Flask CLI commands
@pytest.fixture
def runner(app):
    return app.test_cli_runner()

def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200

def test_health_check_route(client):
    response = client.get('/meta/health/canary')
    assert response.status_code == 204
