# noinspection PyPackageRequirements
import ulid

from enum import Enum

# noinspection PyProtectedMember
# flake8: noqa
from psycopg2._psycopg import Error

# noinspection PyPackageRequirements
from sqlalchemy.exc import SQLAlchemyError
from iso3166 import countries as iso_countries

from arctic_office_projects_api.extensions import db


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
    with open("arctic_office_projects_api/bulk_importer/exception_log.txt", "a") as f:
        f.write(exception_info + "\n")
