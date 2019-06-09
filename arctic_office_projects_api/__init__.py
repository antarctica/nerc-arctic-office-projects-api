from http import HTTPStatus

import sentry_sdk

from flask import Flask, request, has_request_context
from flask import Flask, jsonify
from flask.logging import default_handler

from flask_reverse_proxy_fix.middleware import ReverseProxyPrefixFix
from flask_request_id_header.middleware import RequestID
# noinspection PyPackageRequirements
from werkzeug.exceptions import BadRequest, NotFound, InternalServerError, UnprocessableEntity

from arctic_office_projects_api.utils import healthcheck_db
from config import config
from arctic_office_projects_api.logging import RequestFormatter
from arctic_office_projects_api.extensions import db, auth
from arctic_office_projects_api.errors import error_handler_generic_bad_request, error_handler_generic_not_found, \
    error_handler_generic_internal_server_error, error_handler_generic_unprocessable_entity
from arctic_office_projects_api.main import main as main_blueprint


def create_app(config_name):
    app = Flask(__name__)

    # Config
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Extensions
    db.init_app(app)
    auth.init_app(app=app)

    # Middleware / Wrappers
    if app.config['APP_ENABLE_PROXY_FIX']:
        ReverseProxyPrefixFix(app)
    if app.config['APP_ENABLE_REQUEST_ID']:
        RequestID(app)
    if app.config['APP_ENABLE_SENTRY']:
        sentry_sdk.init(**app.config['SENTRY_CONFIG'])

    # Logging
    formatter = RequestFormatter(
        '[%(asctime)s] [%(levelname)s] [%(request_id)s] [%(url)s] %(module)s: %(message)s'
    )
    default_handler.setFormatter(formatter)
    default_handler.setLevel(app.config['LOGGING_LEVEL'])

    # Error handlers
    app.register_error_handler(BadRequest, error_handler_generic_bad_request)
    app.register_error_handler(NotFound, error_handler_generic_not_found)
    app.register_error_handler(UnprocessableEntity, error_handler_generic_unprocessable_entity)
    app.register_error_handler(InternalServerError, error_handler_generic_internal_server_error)

    app.register_blueprint(main_blueprint)
    # Routes
    app.add_url_rule('/', 'index', index_route)
    app.add_url_rule('/meta/health/canary', 'canary_health_check', healthcheck_canary_route, methods=['get', 'options'])

    # Blueprints

    return app


# Route methods


def index_route():
    """
    Returns a simple welcome message
    """

    payload = {
        'meta': {
            'summary': 'This API is used to record details of projects related to the NERC Arctic Office - '
                       'https://www.arctic.ac.uk'
        }
    }

    return jsonify(payload)


def healthcheck_canary_route():
    """
    Returns whether this service is healthy

    This healthcheck checks the application itself (assumed to be healthy if this method can be executed) and the
    availability of its dependencies, such as databases.

    If healthy a 204 No Content response is returned, if unhealthy a 503 Service Unavailable response is returned. This
    healthcheck is binary and does not return any details to reduce payload size and prevent leaking sensitive data.

    Other healthcheck's should be used where more details are required. This healthcheck is intended for use with load
    balancers to give early indication of a service not being available.
    """
    dependencies = {
        'db': healthcheck_db()
    }

    if False in dependencies.values():
        return '', HTTPStatus.SERVICE_UNAVAILABLE

    return '', HTTPStatus.NO_CONTENT
