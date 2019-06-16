import unittest

from flask_migrate import Config, upgrade, downgrade, Migrate
from flask_azure_oauth.tokens import TestJwt

from arctic_office_projects_api import create_app, auth, db
from arctic_office_projects_api.errors import ApiException
from arctic_office_projects_api.seeding import seed_predictable_test_resources


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
