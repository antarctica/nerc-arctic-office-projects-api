from http import HTTPStatus
from arctic_office_projects_api.version import __version__
from arctic_office_projects_api.utils import healthcheck_db

app_version = __version__


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
