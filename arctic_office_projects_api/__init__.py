import os

import sentry_sdk

from flask import Flask
from flask.logging import default_handler
from werkzeug.middleware.proxy_fix import ProxyFix

# from flask_reverse_proxy_fix.middleware import ReverseProxyPrefixFix
from flask_request_id_header.middleware import RequestID

# noinspection PyPackageRequirements
from werkzeug.exceptions import (
    BadRequest,
    NotFound,
    InternalServerError,
    UnprocessableEntity,
)

from config import config
from arctic_office_projects_api.logging import RequestFormatter
from arctic_office_projects_api.extensions import db, auth
from arctic_office_projects_api.errors import (
    error_handler_generic_bad_request,
    error_handler_generic_not_found,
    error_handler_generic_internal_server_error,
    error_handler_generic_unprocessable_entity,
)
from arctic_office_projects_api.commands import seeding_cli_group, importing_cli_group
from arctic_office_projects_api.routes import index_route, healthcheck_canary_route
from arctic_office_projects_api.resources.projects import projects as projects_blueprint
from arctic_office_projects_api.resources.people import people as people_blueprint
from arctic_office_projects_api.resources.grants import grants as grants_blueprint
from arctic_office_projects_api.resources.organisations import (
    organisations as organisations_blueprint,
)
from arctic_office_projects_api.resources.category_schemes import (
    category_schemes as category_schemes_blueprint,
)
from arctic_office_projects_api.resources.category_terms import (
    category_terms as category_terms_blueprint,
)
from arctic_office_projects_api.resources.participants import (
    participants as participants_blueprint,
)
from arctic_office_projects_api.resources.allocations import (
    allocations as allocations_blueprint,
)
from arctic_office_projects_api.resources.categorisations import (
    categorisations as categorisations_blueprint,
)


def create_app(config_name):
    app = Flask(__name__)

    # Config
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI") or None

    # Extensions
    db.init_app(app)
    auth.init_app(app=app)

    # # Middleware / Wrappers
    if app.config["APP_ENABLE_PROXY_FIX"]:
        app.wsgi_app = ProxyFix(
            app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1
        )
        # ReverseProxyPrefixFix(app)
    if app.config["APP_ENABLE_REQUEST_ID"]:
        RequestID(app)
    if app.config["APP_ENABLE_SENTRY"]:
        sentry_sdk.init(**app.config["SENTRY_CONFIG"])

    # Logging
    formatter = RequestFormatter(
        "[%(asctime)s] [%(levelname)s] [%(request_id)s] [%(url)s]: %(message)s"
    )
    default_handler.setFormatter(formatter)
    default_handler.setLevel(app.config["LOGGING_LEVEL"])

    # Error handlers
    app.register_error_handler(BadRequest, error_handler_generic_bad_request)
    app.register_error_handler(NotFound, error_handler_generic_not_found)
    app.register_error_handler(
        UnprocessableEntity, error_handler_generic_unprocessable_entity
    )
    app.register_error_handler(
        InternalServerError, error_handler_generic_internal_server_error
    )

    # CLI commands
    app.cli.add_command(seeding_cli_group)
    app.cli.add_command(importing_cli_group)

    # Routes
    app.add_url_rule("/", "index", index_route, methods=["get", "options"])
    app.add_url_rule(
        "/meta/health/canary",
        "canary_health_check",
        healthcheck_canary_route,
        methods=["get", "options"],
    )

    # Resource blueprints
    app.register_blueprint(projects_blueprint)
    app.register_blueprint(people_blueprint)
    app.register_blueprint(grants_blueprint)
    app.register_blueprint(organisations_blueprint)
    app.register_blueprint(category_schemes_blueprint)
    app.register_blueprint(category_terms_blueprint)
    app.register_blueprint(participants_blueprint)
    app.register_blueprint(allocations_blueprint)
    app.register_blueprint(categorisations_blueprint)

    return app
