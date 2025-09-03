# noinspection PyPackageRequirements
import ulid
import logging

from enum import Enum

# noinspection PyProtectedMember
# flake8: noqa
from psycopg2._psycopg import Error

# noinspection PyPackageRequirements
from sqlalchemy.exc import SQLAlchemyError
from iso3166 import countries as iso_countries

from arctic_office_projects_api.extensions import db

from flask import has_request_context, request, current_app as app


class RequestFormatter(logging.Formatter):
    def format(self, record):
        record.url = "NA"
        record.request_id = "NA"

        if has_request_context():
            record.url = request.url
            if app.config["APP_ENABLE_REQUEST_ID"]:
                record.request_id = request.environ.get("HTTP_X_REQUEST_ID")

        return super().format(record)


def conditional_decorator(decor, condition):
    def decorator(function):
        if condition:
            # Return the function unchanged, not decorated.
            return function
        return decor(function)

    return decorator


def generate_neutral_id() -> str:
    """
    Generates a new, unique, 'Neutral ID' using ULIDs (Universally Unique Lexicographically Sortable Identifiers):
    https://github.com/ulid/spec

    These IDs are designed to identify resources without relying on implementation specific identifiers, such as
    database auto-incrementing IDs.

    Example Neutral ID: '01D5M0CFQV4M7JASW7F87SRDYB'

    :rtype str
    :return: unique neutral ID
    """
    return ulid.new().str


def generate_countries_enum(*, name: str = "Countries") -> Enum:
    countries = []
    for country in iso_countries:
        countries.append(
            (
                country.alpha3,
                {"name": country.name, "iso_3166_alpha3-code": country.alpha3},
            )
        )

    # noinspection PyArgumentList
    return Enum(name, countries)


def healthcheck_db() -> bool:
    try:
        # Establish a connection
        with db.engine.connect():
            pass
    except SQLAlchemyError as e:  # pragma: no cover
        return False  # pragma: no cover

    return True


def log_exception_to_file(exception_info):
    with open(
        "/usr/src/app/arctic_office_projects_api/bulk_importer/exception_log.txt", "a"
    ) as f:  # pragma: no cover
        f.write(exception_info + "\n")  # pragma: no cover
