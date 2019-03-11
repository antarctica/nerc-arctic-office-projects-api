from psycopg2._psycopg import Error
# noinspection PyPackageRequirements
from sqlalchemy.exc import OperationalError

from arctic_office_projects_api import db


def healthcheck_db() -> bool:
    try:
        # run basic connectivity check
        db.engine.execute('SELECT 1')
    except (Error, OperationalError):
        return False

    return True
