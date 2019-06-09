# noinspection PyPackageRequirements
import ulid

from enum import Enum

# noinspection PyProtectedMember
from psycopg2._psycopg import Error
# noinspection PyPackageRequirements
from sqlalchemy.exc import OperationalError
from iso3166 import countries as iso_countries

from arctic_office_projects_api.extensions import db


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


def generate_countries_enum(*, name: str = 'Countries') -> Enum:
    countries = []
    for country in iso_countries:
        countries.append((country.alpha3, {'name': country.name, 'iso_3166_alpha3-code': country.alpha3}))

    # noinspection PyArgumentList
    return Enum(name, countries)


def healthcheck_db() -> bool:
    try:
        # run basic connectivity check
        db.engine.execute('SELECT 1')
    except (Error, OperationalError):
        return False

    return True
