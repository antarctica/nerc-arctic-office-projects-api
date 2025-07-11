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


def healthcheck_route():
    """
    Returns whether this service is healthy
    """
    dependencies = {"db": healthcheck_db()}

    if False in dependencies.values():
        return "", HTTPStatus.SERVICE_UNAVAILABLE

    return {"value": "ok - arctic office api"}
