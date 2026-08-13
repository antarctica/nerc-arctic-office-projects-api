import pytest
from flask_migrate import Config, upgrade, Migrate

from arctic_office_projects_api import create_app
from arctic_office_projects_api.extensions import db
from arctic_office_projects_api.seeding import seed_predictable_test_resources


@pytest.fixture(scope="function")
def app():
    app = create_app("testing")
    with app.app_context():
        yield app  # Provide the app instance to tests


@pytest.fixture
def client(app):
    return app.test_client()  # Return a test client instance


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture(scope="function")
def db_create(app):
    """Fixture to create the database tables etc."""

    with app.app_context():
        db.create_all()
        config = Config("migrations/alembic.ini")
        config.set_main_option("script_location", "migrations")
        Migrate(app, db)
        upgrade()
        seed_predictable_test_resources()
        db.session.commit()
        yield db
        db.session.remove()
        # db.drop_all()  # Clean up after the test


@pytest.fixture(autouse=True)
def mock_validate_token(monkeypatch):
    import arctic_office_projects_api  # validate_token is in __init__.py

    def fake_validate_token(token):
        return {"sub": "test-user", "roles": ["tester"]}

    # Monkeypatch directly on the module
    monkeypatch.setattr(arctic_office_projects_api, "validate_token", fake_validate_token)
