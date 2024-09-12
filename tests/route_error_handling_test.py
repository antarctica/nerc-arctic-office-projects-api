import pytest
from _pytest.fixtures import FixtureRequest
from flask.testing import FlaskClient
from pytest_httpserver import HTTPServer, RequestMatcher

from flask_entra_auth.exceptions import (
    EntraAuthInsufficientScopesError,
    EntraAuthInvalidAppError,
    EntraAuthInvalidAudienceError,
    EntraAuthInvalidExpirationError,
    EntraAuthInvalidIssuerError,
    EntraAuthInvalidSignatureError,
    EntraAuthInvalidSubjectError,
    EntraAuthInvalidTokenError,
    EntraAuthInvalidTokenVersionError,
    EntraAuthMissingClaimError,
    EntraAuthNotValidBeforeError,
    EntraAuthOidcError,
    EntraAuthRequestInvalidAuthHeaderError,
    EntraAuthRequestNoAuthHeaderError,
    EntraAuthSigningKeyError,
)
from flask_entra_auth.mocks.jwt import MockClaims
# from tests.utils import _assert_entra_error


class TestAppUnrestricted:
    """Test unrestricted route."""

    def test_ok(self, fx_app_client: FlaskClient):
        """Request is successful."""
        response = fx_app_client.get("/unrestricted")
        assert response.status_code == 200
        assert response.text == "Unrestricted route."
