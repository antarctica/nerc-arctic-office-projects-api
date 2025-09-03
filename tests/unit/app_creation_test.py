from flask import Flask


def test_app_creation(app):
    assert isinstance(app, Flask)
