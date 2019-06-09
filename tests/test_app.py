from http import HTTPStatus

from flask import current_app
# noinspection PyPackageRequirements
from sqlalchemy.exc import OperationalError

from tests.base_test import BaseTestCase


class AppTestCase(BaseTestCase):
    def test_app_exists(self):
        self.assertIsNotNone(current_app)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])


class AppIndexTestCase(BaseTestCase):
    def test_index_route(self):
        response = self.client.get(
            '/',
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn('meta', json_response.keys())
        self.assertIn('summary', json_response['meta'].keys())
        self.assertEqual(
            'This API is used to record details of projects related to the NERC Arctic Office - '
            'https://www.arctic.ac.uk',
            json_response['meta']['summary']
        )


class AppMetaTestCase(BaseTestCase):
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
