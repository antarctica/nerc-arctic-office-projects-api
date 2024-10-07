import pytest
from http import HTTPStatus
from flask import Flask, jsonify
from uuid import UUID

from arctic_office_projects_api.errors import (
    AppException,
    ApiException,
    ApiBadRequestError,
    ApiInternalServerError,
    ApiNotFoundError,
    ApiUnprocessableEntityError,
    error_handler_generic_bad_request,
    error_handler_generic_internal_server_error,
    error_handler_generic_not_found,
    error_handler_generic_unprocessable_entity,
)

# Test AppException and ApiException Classes
def test_app_exception_initialization():
    # Test the initialization of AppException and its dict and json methods
    exc = AppException(code="TEST_CODE", title="Test Title", detail="Test Detail", meta={"info": "test"})
    
    assert exc.code == "TEST_CODE"
    assert exc.title == "Test Title"
    assert exc.detail == "Test Detail"
    assert exc.meta == {"info": "test"}
    
    exc_dict = exc.dict()
    assert exc_dict == {
        "title": "Test Title",
        "code": "TEST_CODE",
        "detail": "Test Detail",
        "meta": {"info": "test"}
    }
    
    exc_json = exc.json()
    assert exc_json == '{"title": "Test Title", "code": "TEST_CODE", "detail": "Test Detail", "meta": {"info": "test"}}'

def test_api_exception_initialization():
    # Test ApiException initialization and the dict method
    api_exc = ApiException(
        status=HTTPStatus.BAD_REQUEST,
        code="API_ERROR",
        title="API Error",
        detail="API Error detail",
        meta={"field": "value"},
        about_link="http://example.com/about"
    )
    
    assert api_exc.status == HTTPStatus.BAD_REQUEST
    assert api_exc.code == "API_ERROR"
    assert api_exc.title == "API Error"
    assert api_exc.detail == "API Error detail"
    assert api_exc.meta == {"field": "value"}
    assert api_exc.links == {"about": "http://example.com/about"}
    
    api_dict = api_exc.dict()
    assert api_dict["status"] == HTTPStatus.BAD_REQUEST.value
    assert UUID(api_dict["id"])  # Validate that 'id' is a valid UUID
    assert api_dict["links"] == {"about": "http://example.com/about"}

def test_api_subclass_initialization():
    # Test specific subclasses of ApiException
    bad_request_exc = ApiBadRequestError()
    internal_error_exc = ApiInternalServerError()
    not_found_exc = ApiNotFoundError()
    unprocessable_entity_exc = ApiUnprocessableEntityError()

    assert bad_request_exc.status == HTTPStatus.BAD_REQUEST
    assert bad_request_exc.title == "Bad Request"
    assert bad_request_exc.detail == "Check your request and try again"

    assert internal_error_exc.status == HTTPStatus.INTERNAL_SERVER_ERROR
    assert not_found_exc.status == HTTPStatus.NOT_FOUND
    assert unprocessable_entity_exc.status == HTTPStatus.UNPROCESSABLE_ENTITY

# Test Flask Error Handlers
@pytest.fixture
def app():
    app = Flask(__name__)
    
    # Register error handlers for specific HTTP status codes and custom exceptions
    app.register_error_handler(HTTPStatus.BAD_REQUEST, error_handler_generic_bad_request)
    app.register_error_handler(HTTPStatus.INTERNAL_SERVER_ERROR, error_handler_generic_internal_server_error)
    app.register_error_handler(HTTPStatus.NOT_FOUND, error_handler_generic_not_found)
    app.register_error_handler(HTTPStatus.UNPROCESSABLE_ENTITY, error_handler_generic_unprocessable_entity)
    
    # Explicitly register handlers for custom exceptions
    app.register_error_handler(ApiBadRequestError, error_handler_generic_bad_request)
    app.register_error_handler(ApiInternalServerError, error_handler_generic_internal_server_error)
    app.register_error_handler(ApiNotFoundError, error_handler_generic_not_found)
    app.register_error_handler(ApiUnprocessableEntityError, error_handler_generic_unprocessable_entity)

    return app

def test_bad_request_error_handler(app):
    with app.test_client() as client:
        @app.route('/bad_request')
        def bad_request():
            raise ApiBadRequestError()

        response = client.get('/bad_request')
        assert response.status_code == HTTPStatus.BAD_REQUEST
        data = response.get_json()
        assert "errors" in data
        assert data["errors"][0]["title"] == "Bad Request"

def test_internal_server_error_handler(app):
    with app.test_client() as client:
        @app.route('/internal_server_error')
        def internal_error():
            raise ApiInternalServerError()

        response = client.get('/internal_server_error')
        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        data = response.get_json()
        assert "errors" in data
        assert data["errors"][0]["title"] == "Internal Server Error"

def test_not_found_error_handler(app):
    with app.test_client() as client:
        @app.route('/not_found')
        def not_found():
            raise ApiNotFoundError()

        response = client.get('/not_found')
        assert response.status_code == HTTPStatus.NOT_FOUND
        data = response.get_json()
        assert "errors" in data
        assert data["errors"][0]["title"] == "Not Found"

def test_unprocessable_entity_error_handler(app):
    with app.test_client() as client:
        @app.route('/unprocessable_entity')
        def unprocessable_entity():
            raise ApiUnprocessableEntityError()

        response = client.get('/unprocessable_entity')
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        data = response.get_json()
        assert "errors" in data
        assert data["errors"][0]["title"] == "Unprocessable Entity"
