from http import HTTPStatus
from importlib.metadata import version

from arctic_office_projects_api.utils import healthcheck_db

app_version = version("arctic_office_projects_api")


def index_route():
    """
    Returns a simple welcome message
    """
    return {"value": "This API is used to record details of projects related to the NERC Arctic Office - "
            "https://www.arctic.ac.uk"}


def healthcheck_route():
    """healthcheck"""
    dependencies = {"db": healthcheck_db()}

    if False in dependencies.values():
        return "", HTTPStatus.SERVICE_UNAVAILABLE  # pragma: no cover

    return {"value": f"ok - arctic office projects database api - {app_version}"}
