import unittest
from unittest.mock import patch

from flask_migrate import Config, upgrade, downgrade, Migrate

# from flask_azure_oauth import FlaskAzureOauth
# from flask_azure_oauth.mocks.keys import TestJwk as TestJwk_key
# from flask_azure_oauth.mocks.tokens import TestJwt as TestJwt_token

from flask_entra_auth.resource_protector import FlaskEntraAuth
from flask_entra_auth.mocks.jwt import MockClaims as TestJwt_token
from flask_entra_auth.mocks.jwks import MockJwk as TestJwk_key

from arctic_office_projects_api import create_app, db
from arctic_office_projects_api.errors import ApiException
from arctic_office_projects_api.seeding import seed_predictable_test_resources


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.test_jwks = TestJwk_key()

        with patch.object(FlaskEntraAuth, "_signing_key") as mocked_get_jwks:

            mocked_get_jwks.return_value = self.test_jwks.jwks()

            # `self.app` should be set to a Flask application, either by direct import, or by calling an app factory
            self.app = create_app('testing')

            self.app.config["TEST_JWKS"] = self.test_jwks
            self.app_context = self.app.app_context()
            self.app_context.push()
            self.client = self.app.test_client()

    def tearDown(self):
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
        jwt = TestJwt_token(app=self.app, scps=scopes)
        return jwt.dumps()


class BaseResourceTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()

        with self.app.app_context():
            # Migrate and seed database
            config = Config("migrations/alembic.ini")
            config.set_main_option("script_location", "migrations")
            Migrate(self.app, db)
            upgrade()
            seed_predictable_test_resources()
            db.session.commit()

    def tearDown(self):
        db.session.remove()
        with self.app.app_context():
            # Rollback all DB migrations
            downgrade(revision='base')

        super().tearDown()


class BaseCommandTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()

        with self.app.app_context():
            # Migrate database
            config = Config("migrations/alembic.ini")
            config.set_main_option("script_location", "migrations")
            Migrate(self.app, db)
            upgrade()

        self.runner = self.app.test_cli_runner()

    def tearDown(self):
        db.session.remove()
        with self.app.app_context():
            # Rollback all DB migrations
            downgrade(revision='base')

        super().tearDown()
