import unittest

from http import HTTPStatus

from flask_migrate import Config, upgrade, downgrade, Migrate
from arctic_office_projects_api.errors import ApiException

from arctic_office_projects_api.meta.errors import ApiNotFoundError
from arctic_office_projects_api import create_app, db
from arctic_office_projects_api.models import Project


class MainBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

        with self.app.app_context():
            # Migrate and seed database
            config = Config("migrations/alembic.ini")
            config.set_main_option("script_location", "migrations")
            Migrate(self.app, db)
            upgrade()
            Project.seed(quantity=5)
            db.session.commit()

        self.maxDiff = None

    def tearDown(self):
        db.session.remove()
        self.app_context.pop()

        with self.app.app_context():
            # Rollback all DB migrations
            downgrade(revision='base')

    @staticmethod
    def _prepare_expected_error_payload(error: ApiException):
        error = error.dict()
        # Overwrite dynamic error ID with static value to allow comparision
        error['id'] = 'a611b89f-f1bb-43c5-8efa-913c83c9109e'

        return {'errors': [error]}

    @staticmethod
    def _prepare_error_response(json_response: dict) -> dict:
        # Overwrite dynamic error ID with static value to allow comparision
        if 'id' in json_response['errors'][0].keys():
            json_response['errors'][0]['id'] = 'a611b89f-f1bb-43c5-8efa-913c83c9109e'

        return json_response

    def test_index(self):
        response = self.client.get(
            '/',
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn('meta', json_response.keys())
        self.assertIn('summary', json_response['meta'].keys())
        self.assertEqual(
            'xxx',
            json_response['meta']['summary']
        )

    def test_projects_list(self):
        # expected_payload_data_item = {
        #     'attributes': {
        #         'title': 'xxx'
        #     },
        #     'id': '01D5M0CFQV4M7JASW7F87SRDYB',
        #     'links': {
        #         'self': 'http://localhost:9000/projects/01D5M0CFQV4M7JASW7F87SRDYB'
        #     },
        #     'type': 'project'
        # }
        expected_payload_links = {
            'first': 'http://localhost:9000/projects?page=1',
            'prev': None,
            'self': 'http://localhost:9000/projects?page=1',
            'next': 'http://localhost:9000/projects?page=2',
            'last': 'http://localhost:9000/projects?page=3'
        }

        response = self.client.get(
            '/projects',
            base_url='http://localhost:9000',
            query_string={
                'page': 1
            }
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIn('data', json_response.keys())
        self.assertEqual(len(json_response['data']), 2)
        # self.assertDictEqual(json_response['data'][0], expected_payload_data_item)
        self.assertIn('links', json_response.keys())
        self.assertDictEqual(json_response['links'], expected_payload_links)

    def test_people_sensitive_detail(self):
        # expected_payload = {
        #     'data': {
        #         'attributes': {
        #             'title': 'xxx'
        #         },
        #         'id': '01D5M0CFQV4M7JASW7F87SRDYB',
        #         'links': {
        #             'self': 'http://localhost:9000/projects/01D5M0CFQV4M7JASW7F87SRDYB'
        #         },
        #         'type': 'project'
        #     },
        #     'links': {
        #         'self': 'http://localhost:9000/projects/01D5M0CFQV4M7JASW7F87SRDYB'
        #     }
        # }

        response = self.client.get(
            '/projects/01D5M0CFQV4M7JASW7F87SRDYB',
            base_url='http://localhost:9000'
        )
        json_response = response.get_json()
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIn('data', json_response.keys())
        # self.assertDictEqual(json_response, expected_payload)

    def test_people_sensitive_single_missing_unknown_id(self):
        error = ApiNotFoundError()
        expected_payload = self._prepare_expected_error_payload(error)

        for project_id in ['', 'unknown']:
            with self.subTest(project_id=project_id):
                response = self.client.get(
                    f"/projects/{ project_id }",
                    base_url='http://localhost:9000'
                )
                json_response = response.get_json()
                json_response = self._prepare_error_response(json_response)
                self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)
                self.assertDictEqual(json_response, expected_payload)
