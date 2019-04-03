from http import HTTPStatus

from flask import Blueprint

from arctic_office_projects_api.meta.utils import healthcheck_db


meta = Blueprint('meta', __name__)


@meta.route('/meta/health/canary', methods=['get', 'options'])
def meta_healthcheck_canary():
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
