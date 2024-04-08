import os
import logging
from logging import StreamHandler

# noinspection PyPackageRequirements
from dotenv import load_dotenv
from sentry_sdk.integrations.flask import FlaskIntegration
from str2bool import str2bool


class Config(object):
    @staticmethod
    def init_app(app):
        # Log to stderr
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    DEBUG = False
    TESTING = False

    APP_ENABLE_SENTRY = str2bool(os.environ.get('APP_ENABLE_SENTRY')) or True
    APP_ENABLE_REQUEST_ID = str2bool(os.environ.get('APP_ENABLE_REQUEST_ID')) or True
    APP_ENABLE_PROXY_FIX = str2bool(os.environ.get('APP_ENABLE_PROXY_FIX')) or True

    LOGGING_LEVEL = logging.WARNING

    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or None
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS') or False

    SERVER_NAME = os.getenv('SERVER_NAME') or None
    PREFERRED_URL_SCHEME = os.getenv('PREFERRED_URL_SCHEME') or 'https'
    REVERSE_PROXY_PATH = os.getenv('REVERSE_PROXY_PATH') or None
    REQUEST_ID_UNIQUE_VALUE_PREFIX = os.getenv('REQUEST_ID_UNIQUE_VALUE_PREFIX') or 'BAS-API-LB-RV1'

    APP_PAGE_SIZE = int(os.getenv('APP_PAGE_SIZE') or 10)

    AZURE_OAUTH_TENANCY = os.getenv('AZURE_OAUTH_TENANCY') or None
    AZURE_OAUTH_APPLICATION_ID = os.getenv('AZURE_OAUTH_APPLICATION_ID') or None
    AZURE_OAUTH_CLIENT_APPLICATION_IDS = str(os.getenv('AZURE_OAUTH_CLIENT_APPLICATION_IDS') or '').split(',') or []

    SENTRY_CONFIG = {
        'integrations': [FlaskIntegration()],
        'environment': os.getenv('FLASK_ENV') or 'default'
    }
    if 'APP_RELEASE' in os.environ:
        SENTRY_CONFIG['release'] = os.environ.get('APP_RELEASE')


class TestConfig(Config):
    ENV = 'testing'

    DEBUG = True
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False

    APP_ENABLE_SENTRY = str2bool(os.environ.get('APP_ENABLE_SENTRY')) or False

    LOGGING_LEVEL = logging.DEBUG

    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or 'postgresql://app:password@app-db/app_test'

    PREFERRED_URL_SCHEME = os.getenv('PREFERRED_URL_SCHEME') or 'http'

    APP_PAGE_SIZE = 2

    # AZURE_OAUTH_TENANCY = 'testing'
    # AZURE_OAUTH_APPLICATION_ID = 'testing'
    # AZURE_OAUTH_CLIENT_APPLICATION_IDS = ['testing']


class DevelopmentConfig(Config):
    DEBUG = True

    APP_ENABLE_SENTRY = str2bool(os.environ.get('APP_ENABLE_SENTRY')) or False
    APP_ENABLE_PROXY_FIX = str2bool(os.environ.get('APP_ENABLE_PROXY_FIX')) or False

    LOGGING_LEVEL = logging.INFO

    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or 'postgresql://app:password@app-db/app'

    SERVER_NAME = os.getenv('SERVER_NAME') or 'localhost:9000'
    PREFERRED_URL_SCHEME = os.getenv('PREFERRED_URL_SCHEME') or 'http'


class ReviewConfig(Config):
    LOGGING_LEVEL = logging.INFO

    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or os.getenv('DATABASE_URL')


class StagingConfig(Config):
    LOGGING_LEVEL = logging.INFO

    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or os.getenv('DATABASE_URL')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or os.getenv('DATABASE_URL')


config = {
    'testing': TestConfig,
    'development': DevelopmentConfig,
    'review': ReviewConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
    'default': ProductionConfig
}
