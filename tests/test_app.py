from flask import current_app

from tests.base_test import BaseTestCase


class AppTestCase(BaseTestCase):
    def test_app_exists(self):
        self.assertIsNotNone(current_app)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])
