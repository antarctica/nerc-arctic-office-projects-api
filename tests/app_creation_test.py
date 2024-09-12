import pytest
from flask import Flask
from arctic_office_projects_api import create_app

@pytest.fixture
def app():
    app = create_app('testing')
    app.config.update({
        'TESTING': True,
    })
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_app_creation(app):
    assert isinstance(app, Flask)
    assert app.config['TESTING'] is True
