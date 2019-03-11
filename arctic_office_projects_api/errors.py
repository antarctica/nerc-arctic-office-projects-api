import json
from http import HTTPStatus
from uuid import uuid4

from flask import make_response, jsonify, Response


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
        :param code: Application specific identifier for the error that SHOULD NOT change between instances
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
        :return: Error as dict
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
