from http import HTTPStatus

# noinspection PyPackageRequirements
from sqlalchemy.exc import OperationalError

from tests.base_test import BaseTestCase


class MetaBlueprintTestCase(BaseTestCase):
    def test_meta_healthcheck_canary_success(self):
        for method in ['get', 'options']:
            with self.subTest(method=method):
                if method == 'get':
                    response = self.client.get(
                        '/meta/health/canary',
                        base_url='http://localhost:9000'
                    )
                elif method == 'options':
                    response = self.client.options(
                        '/meta/health/canary',
                        base_url='http://localhost:9000'
                    )
                else:
                    raise NotImplementedError("HTTP method not supported")

                self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)

    def test_meta_healthcheck_canary_failure_db(self):
        # Break database connection (wrong database)
        db_url = self.app.config['SQLALCHEMY_DATABASE_URI']
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://app:password@app-db/invalid-database'

        for method in ['get', 'options']:
            with self.subTest(method=method):
                try:
                    if method == 'get':
                        response = self.client.get(
                            '/meta/health/canary',
                            base_url='http://localhost:9000'
                        )
                    elif method == 'options':
                        response = self.client.options(
                            '/meta/health/canary',
                            base_url='http://localhost:9000'
                        )
                    else:
                        raise NotImplementedError("HTTP method not supported")
                except OperationalError:
                    # noinspection PyUnboundLocalVariable
                    self.assertEqual(response.status_code, HTTPStatus.SERVICE_UNAVAILABLE)

        # Restore real database connection
        self.app.config['SQLALCHEMY_DATABASE_URI'] = db_url
