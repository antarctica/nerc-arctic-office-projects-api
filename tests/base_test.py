import unittest

from flask_azure_oauth.tokens import TestJwt

from arctic_office_projects_api import create_app, auth
from arctic_office_projects_api.errors import ApiException


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

        self.maxDiff = None

    def tearDown(self):
        auth.reset_app()
        self.app_context.pop()

    @staticmethod
    def util_prepare_expected_error_payload(error: ApiException):
        error = error.dict()
        # Overwrite dynamic error ID with static value to allow comparision
        error['id'] = 'a611b89f-f1bb-43c5-8efa-913c83c9109e'

        return {'errors': [error]}

    @staticmethod
    def util_prepare_error_response(json_response: dict) -> dict:
        # Overwrite dynamic error ID with static value to allow comparision
        if 'id' in json_response['errors'][0].keys():
            json_response['errors'][0]['id'] = 'a611b89f-f1bb-43c5-8efa-913c83c9109e'

        return json_response

    def util_create_auth_token(self, *, scopes: list = None):
        jwt = TestJwt(app=self.app, scopes=scopes)
        return jwt.dumps()
