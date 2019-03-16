from http import HTTPStatus

from flask import Response
# noinspection PyPackageRequirements
from werkzeug.exceptions import BadRequest, NotFound, InternalServerError, Conflict

from arctic_office_projects_api.errors import ApiException


class APiBadRequestError(ApiException):
    """
    Represents a generic request error
    """
    status = HTTPStatus.BAD_REQUEST
    title = 'Bad Request'
    detail = 'Check your request and try again'


class APiInternalServerError(ApiException):
    """
    Represents a generic internal error
    """
    status = HTTPStatus.INTERNAL_SERVER_ERROR
    title = 'Internal Server Error'
    detail = 'Please try again in a few minutes or seek support'


class ApiNotFoundError(ApiException):
    """
    Represents a generic not found error
    """
    status = HTTPStatus.NOT_FOUND
    title = 'Not Found'
    detail = 'The requested URL was not found, check the address and try again'


class ApiConflictError(ApiException):
    """
    Represents a generic conflict error
    """
    status = HTTPStatus.CONFLICT
    title = 'Conflict'
    detail = 'The requested URL could not be resolved to a single entity, check the address and try again'


# noinspection PyUnusedLocal
def error_handler_generic_bad_request(e: BadRequest) -> Response:
    """
    Flask error handler for '400 Bad Request' errors

    :type e: BadRequest
    :param e: Exception

    :return: Flask response
    """
    error = APiBadRequestError()
    return error.response()


# noinspection PyUnusedLocal
def error_handler_generic_internal_server_error(e: InternalServerError) -> Response:
    """
    Flask error handler for '500 Internal Server Error' errors

    :type e: InternalServerError
    :param e: Exception

    :return: Flask response
    """
    error = APiInternalServerError()
    return error.response()


# noinspection PyUnusedLocal
def error_handler_generic_not_found(e: NotFound) -> Response:
    """
    Flask error handler for '404 Not Found' errors

    :type e: NotFound
    :param e: Exception

    :return: Flask response
    """
    error = ApiNotFoundError()
    return error.response()


# noinspection PyUnusedLocal
def error_handler_generic_conflict(e: Conflict) -> Response:
    """
    Flask error handler for '409 Conflict' errors

    :type e: Conflict
    :param e: Exception

    :return: Flask response
    """
    error = ApiConflictError()
    return error.response()
