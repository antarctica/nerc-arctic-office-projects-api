from http import HTTPStatus

from flask import jsonify

from arctic_office_projects_api.utils import healthcheck_db


def index_route():
    """
    Returns a simple welcome message
    """
    payload = {
        "meta": {
            "summary": "This API is used to record details of projects related to the NERC Arctic Office - "
            "https://www.arctic.ac.uk"
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
    dependencies = {"db": healthcheck_db()}

    if False in dependencies.values():
        return "", HTTPStatus.SERVICE_UNAVAILABLE

    return "", HTTPStatus.NO_CONTENT
