import json
from http import HTTPStatus
from uuid import uuid4

from flask import make_response, jsonify, Response
# noinspection PyPackageRequirements
from werkzeug.exceptions import BadRequest, NotFound, InternalServerError, UnprocessableEntity


class ApiException(Exception):
    """
    Base API Exception class for representing API errors returned to clients

    All errors in this application should inherit from this class. Errors are structured according to the JSON API
    specification, https://jsonapi.org/format/#error-objects.

    In most cases error specifics can be specified when creating each class instance and the 'response()' method called
    to return the error as a Flask response. Where further processing or handling of the error is needed the 'json()'
    method can be used to return the error as a dict.
    """
    status = HTTPStatus.INTERNAL_SERVER_ERROR
    code = None
    title = 'API Error'
    detail = None
    meta = {}
    links = {}

    def __init__(
        self,
        *,
        status: HTTPStatus = None,
        code: str = None,
        title: str = None,
        detail: str = None,
        meta: dict = None,
        about_link: str = None
    ):
        """
        :type status: HTTPStatus
        :param status: HTTP Status, as specified by members of the http.HTTPStatus enum
        :type code: str
        :param code: application specific identifier for the error that SHOULD NOT change between instances
        :type title: str
        :param title: short, human-readable summary of the error that SHOULD NOT change between instances
        :type detail: str
        :param detail: more detailed, or instance specific, human readable information about the error
        :type meta: dict
        :param meta: additional, free-form information about the error, possibly machine readable
        :param about_link: a URI that leads to more information about the error, either generally or instance specific
        """
        self.id = uuid4()

        if status is not None:
            self.status = status
        if code is not None:
            self.code = code
        if title is not None:
            self.title = title
        if detail is not None:
            self.detail = detail
        if meta is not None:
            self.meta = meta
        if about_link is not None:
            self.links = {
                'about': about_link
            }

    def dict(self) -> dict:
        """
        Formats the error as a dictionary

        :rtype dict
        :return: error as dict
        """
        error = {
            'id': str(self.id),
            'status': self.status.value,
            'title': self.title
        }

        if self.code is not None:
            error['code'] = self.code
        if self.detail is not None:
            error['detail'] = self.detail
        if self.meta:
            error['meta'] = self.meta
        if 'about' in self.links.keys():
            error['links'] = {'about': self.links['about']}

        return error

    def json(self) -> str:
        """
        Formats the error as a JSON serialised string

        :rtype str
        :return: JSON serialised error
        """

        return json.dumps(self.dict())

    def response(self) -> Response:
        """
        Returns the error as a JSON formatted response

        :rtype Response
        :return: Flask response containing the error, formatted as JSON
        """
        payload = {
            'errors': [self.dict()]
        }
        return make_response(jsonify(payload), self.status.value)


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


class ApiUnprocessableEntityError(ApiException):
    """
    Represents a generic unprocessable entity error
    """
    status = HTTPStatus.UNPROCESSABLE_ENTITY
    title = 'Unprocessable Entity'
    detail = 'Your request could not be processed, check your request or seek support'


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
def error_handler_generic_unprocessable_entity(e: UnprocessableEntity) -> Response:
    """
    Flask error handler for '422 Unprocessable Entity' errors

    :type e: UnprocessableEntity
    :param e: Exception

    :return: Flask response
    """
    error = ApiUnprocessableEntityError()
    return error.response()
