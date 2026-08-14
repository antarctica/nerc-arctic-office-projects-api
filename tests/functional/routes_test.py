import os
import json
import tempfile
import pytest

from pathlib import Path
from unittest.mock import patch, call, MagicMock, mock_open
from arctic_office_projects_api import create_app
from arctic_office_projects_api import validate_token

from arctic_office_projects_api.extensions import db
from arctic_office_projects_api.models import Project_Organisations
from arctic_office_projects_api.models import Project_People
from arctic_office_projects_api.models import Project_Subjects
from arctic_office_projects_api.models import Project_Topics


@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client


@pytest.fixture
def temp_log_file():
    # Create a temporary log file
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
        f.write("This is a test exception log\nAnother line")
        temp_path = f.name
    os.environ["IMPORT_EXCEPTION_LOG"] = temp_path
    yield temp_path
    # Clean up
    os.remove(temp_path)


@pytest.fixture
def app_context(client):
    with client.application.app_context():
        yield


def test_validate_token_success(monkeypatch):
    # Patch environment variables
    monkeypatch.setenv("ENTRA_AUTH_TENANT_ID", "tenant123")
    monkeypatch.setenv("ENTRA_AUTH_CLIENT_ID", "client123")

    fake_key = MagicMock()
    fake_key.key = "public-key"

    # Patch PyJWKClient
    with patch("arctic_office_projects_api.PyJWKClient") as mock_jwk_client, \
         patch("arctic_office_projects_api.jwt.decode", return_value={"sub": "user123"}) as mock_jwt_decode:
        mock_jwk = mock_jwk_client.return_value
        mock_jwk.get_signing_key_from_jwt.return_value = fake_key

        decoded = validate_token("fake.jwt.token")

        # Assertions
        mock_jwk_client.assert_called_once_with(
            "https://login.microsoftonline.com/tenant123/discovery/v2.0/keys"
        )
        mock_jwk.get_signing_key_from_jwt.assert_called_once_with("fake.jwt.token")
        mock_jwt_decode.assert_called_once_with(
            "fake.jwt.token",
            "public-key",
            algorithms=["RS256"],
            audience="client123",
            issuer="https://login.microsoftonline.com/tenant123/v2.0",
        )
        assert decoded == {"sub": "user123"}


def test_validate_token_missing_env(monkeypatch):
    monkeypatch.delenv("ENTRA_AUTH_TENANT_ID", raising=False)
    monkeypatch.delenv("ENTRA_AUTH_CLIENT_ID", raising=False)

    with pytest.raises(Exception, match="Missing TENANT_ID or CLIENT_ID"):
        validate_token("fake.jwt.token")


def test_validate_token_invalid_signature(monkeypatch):
    monkeypatch.setenv("ENTRA_AUTH_TENANT_ID", "tenant123")
    monkeypatch.setenv("ENTRA_AUTH_CLIENT_ID", "client123")

    fake_key = MagicMock()
    fake_key.key = "public-key"

    with patch("arctic_office_projects_api.PyJWKClient") as mock_jwk_client, \
         patch("arctic_office_projects_api.jwt.decode", side_effect=Exception("Invalid signature")):
        mock_jwk = mock_jwk_client.return_value
        mock_jwk.get_signing_key_from_jwt.return_value = fake_key

        with pytest.raises(Exception, match="Invalid signature"):
            validate_token("fake.jwt.token")


def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 200


def test_health_check_route(client):
    response = client.get("/healthcheck")
    assert response.status_code == 200


def test_exception_log_success(client, temp_log_file, monkeypatch):
    # Patch the auth decorator to skip auth for testing
    monkeypatch.setattr("arctic_office_projects_api.validate_token", lambda token: {"sub": "test-user"})

    response = client.get(
        "/exception-log",
        headers={"Authorization": "Bearer fake_token"}
    )

    assert response.status_code == 200
    assert response.mimetype == "text/plain"
    assert "This is a test exception log" in response.get_data(as_text=True)


def test_exception_log_not_found(client, monkeypatch):
    # Patch auth
    monkeypatch.setattr("arctic_office_projects_api.validate_token", lambda token: {"sub": "test-user"})
    # Set environment variable to a nonexistent file
    os.environ["IMPORT_EXCEPTION_LOG"] = "/tmp/nonexistent.log"

    response = client.get(
        "/exception-log",
        headers={"Authorization": "Bearer fake_token"}
    )

    assert response.status_code == 404
    assert response.get_data(as_text=True) == "Log file not found"
    assert response.mimetype == "text/plain"


def test_post_gtr_grant_single_success(client, monkeypatch):
    # Patch auth decorator / token validation
    monkeypatch.setattr("arctic_office_projects_api.validate_token", lambda token: {"sub": "test-user"})

    # Patch the import function to avoid actually importing
    with patch(
        "arctic_office_projects_api.import_gateway_to_research_grant_interactively"
    ) as mock_import:
        payload = {"grant-reference": "NE/K011820/1", "lead-project": 1}
        response = client.post(
            "/post-gtr-grant-single",
            json=payload,
            headers={"Authorization": "Bearer fake_token"}
        )

        # Assert that the import function was called with correct args
        mock_import.assert_called_once_with("NE/K011820/1", 1)

        # Assert response
        assert response.status_code == 201
        data = response.get_json()
        assert data["message"] == "Grant post attempted - check import-error log for issues"
        assert data["data"] == payload


def test_post_gtr_grant_single_no_json(client, monkeypatch):
    monkeypatch.setattr("arctic_office_projects_api.validate_token", lambda token: {"sub": "test-user"})

    response = client.post(
        "/post-gtr-grant-single",
        json={},
        headers={"Authorization": "Bearer fake_token"}
    )

    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "No JSON body provided"


def test_post_gtr_grant_bulk_success(client, monkeypatch):
    monkeypatch.setattr(
        "arctic_office_projects_api.validate_token",
        lambda token: {"sub": "test-user"}
    )

    with patch(
        "arctic_office_projects_api.import_gateway_to_research_grant_interactively"
    ) as mock_import:

        payload = [
            {"grant-reference": "NE/K011820/1", "lead-project": 1},
            {"grant-reference": "NE/K011222/1", "lead-project": 0}
        ]

        response = client.post(
            "/post-gtr-grant-bulk",
            json=payload,
            headers={"Authorization": "Bearer fake_token"}
        )

        expected_calls = [
            call("NE/K011820/1", 1),
            call("NE/K011222/1", 0)
        ]
        mock_import.assert_has_calls(expected_calls, any_order=False)
        assert mock_import.call_count == 2

        # Assert response
        assert response.status_code == 201
        data = response.get_json()
        assert data["message"] == "All grants attempted - check import-error log for issues"
        assert data["data"] == payload


def test_post_gtr_grant_bulk_no_json(client, monkeypatch):
    monkeypatch.setattr("arctic_office_projects_api.validate_token", lambda token: {"sub": "test-user"})

    response = client.post(
        "/post-gtr-grant-bulk",
        json=[],
        headers={"Authorization": "Bearer fake_token"}
    )

    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "No JSON body provided"


def test_post_organisations_success(client, monkeypatch):
    # Mock auth
    monkeypatch.setattr("arctic_office_projects_api.validate_token", lambda token: {"sub": "test-user"})

    # Example POST JSON data
    payload = {
        "organisations": [
            {
                "name": "University of Leeds",
                "grid-identifier": "https://www.grid.ac/institutes/grid.9909.9",
                "ror-identifier": "https://api.ror.org/organizations?query=024mrxd33",
                "website": "https://www.leeds.ac.uk"
            },
            {
                "name": "University of Sheffield",
                "grid-identifier": "https://www.grid.ac/institutes/grid.11835.3e",
                "ror-identifier": "https://api.ror.org/organizations?query=05krs5044",
                "website": "https://www.sheffield.ac.uk"
            }
        ]
    }

    # Mock schema file content
    schema_data = {"type": "object", "properties": {"organisations": {"type": "array"}}}

    # Patch open to return schema content
    with patch("builtins.open", mock_open(read_data=json.dumps(schema_data))):
        # Patch db session
        with patch("arctic_office_projects_api.db.session.query") as mock_query, \
             patch("arctic_office_projects_api.db.session.add") as mock_add, \
             patch("arctic_office_projects_api.db.session.commit") as mock_commit, \
             patch("arctic_office_projects_api.utils.generate_neutral_id", side_effect=["id1", "id2"]):

            # Make scalar() return False for every query (organisations not in DB)
            mock_query.return_value.scalar.return_value = False

            response = client.post(
                "/post-organisations",
                json=payload,
                headers={"Authorization": "Bearer fake_token"}
            )

            # Assert DB methods called
            assert mock_add.call_count == 2
            mock_commit.assert_called_once()

            # Assert response
            assert response.status_code == 201
            data = response.get_json()
            assert data["message"] == "Bulk organisations post attempted - check import-error log for issues"


def test_post_organisations_no_json(client, monkeypatch):
    monkeypatch.setattr("arctic_office_projects_api.validate_token", lambda token: {"sub": "test-user"})

    response = client.post(
        "/post-organisations",
        json={},
        headers={"Authorization": "Bearer fake_token"}
    )

    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "No JSON body provided"


def test_post_organisations_schema_not_found(client, monkeypatch):
    monkeypatch.setattr("arctic_office_projects_api.validate_token", lambda token: {"sub": "test-user"})
    monkeypatch.setenv("ORGANISATIONS_SCHEMA_FILE_PATH", "/tmp/nonexistent_schema.json")

    response = client.post(
        "/post-organisations",
        json={"organisations": []},
        headers={"Authorization": "Bearer fake_token"}
    )

    assert response.status_code == 500
    data = response.get_json()
    assert "Schema file not found" in data["error"]


def test_post_organisations_invalid_schema(client, monkeypatch):
    monkeypatch.setattr("arctic_office_projects_api.validate_token", lambda token: {"sub": "test-user"})

    schema_path = Path("/tmp/fake_schema.json")
    monkeypatch.setenv("ORGANISATIONS_SCHEMA_FILE_PATH", str(schema_path))

    # Patch Path.open to return invalid JSON
    with patch("pathlib.Path.open", mock_open(read_data="{invalid json")):
        response = client.post(
            "/post-organisations",
            json={"organisations": []},
            headers={"Authorization": "Bearer fake_token"}
        )

    assert response.status_code == 500
    data = response.get_json()
    assert data["error"] == "Schema file is not valid JSON"


def test_post_categories_success(client, app_context, monkeypatch):
    # Patch authentication
    monkeypatch.setattr("arctic_office_projects_api.validate_token", lambda token: {"sub": "test-user"})

    # Example POST JSON data
    payload = {
        "schemes": [
            {
                "namespace": "ns1",
                "title": "Scheme One",
                "root-concepts": ["concept1", "concept2"]
            }
        ],
        "terms": [
            {
                "subject": "ns1",
                "pref-label": "Term One",
                "path": ["root", "child"],
                "scheme": "ns1"
            }
        ]
    }

    # Mock schema file content
    schema_data = {
        "type": "object",
        "properties": {
            "schemes": {"type": "array"},
            "terms": {"type": "array"}
        }
    }

    # Patch Path.open to return schema content
    with patch("pathlib.Path.open", mock_open(read_data=json.dumps(schema_data))):
        with patch("arctic_office_projects_api.db.session.add") as mock_add, \
             patch("arctic_office_projects_api.db.session.commit") as mock_commit, \
             patch("arctic_office_projects_api.db.session.query") as mock_query, \
             patch("arctic_office_projects_api.generate_neutral_id", side_effect=["id1", "id2"]), \
             patch("arctic_office_projects_api.generate_category_term_ltree_path", side_effect=lambda x: ".".join(x)), \
             patch("arctic_office_projects_api.CategoryScheme.query") as mock_scheme_query:

            # db.session.query(...).scalar() returns False (so all schemes/terms are new)
            mock_query.return_value.scalar.return_value = False

            # Patch CategoryScheme.query.filter_by(...).one() to return a mock scheme
            mock_scheme_query.filter_by.return_value.one.return_value = MagicMock()

            response = client.post(
                "/post-categories",
                json=payload,
                headers={"Authorization": "Bearer fake_token"}
            )

            # Ensure db.session.add called for each scheme and term
            assert mock_add.call_count == 2  # 1 scheme + 1 term
            # Ensure commit called at least once
            assert mock_commit.called

            # Assert response
            assert response.status_code == 201
            data = response.get_json()
            assert data["message"] == "Categories post attempted - check import-error log for issues"


def test_post_categories_no_json(client, monkeypatch):
    monkeypatch.setattr("arctic_office_projects_api.validate_token", lambda token: {"sub": "test-user"})

    response = client.post(
        "/post-categories",
        json={},
        headers={"Authorization": "Bearer fake_token"}
    )

    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "No JSON body provided"


def test_post_organisation_data_success(client, app_context, monkeypatch):
    # Patch authentication
    monkeypatch.setattr("arctic_office_projects_api.validate_token", lambda token: {"sub": "test-user"})

    payload = {
        "organisation_id": "org1",
        "organisation_name": "Organisation One",
        "organisation_ror": "ror1"
    }

    with patch("arctic_office_projects_api.db.session.add") as mock_add, \
         patch("arctic_office_projects_api.db.session.commit") as mock_commit:

        response = client.post(
            "/post-organisation-data",
            json=payload,
            headers={"Authorization": "Bearer fake_token"}
        )

        # Ensure db.session methods were called
        mock_add.assert_called_once()
        mock_commit.assert_called_once()

        # Assert response
        assert response.status_code == 201
        data = response.get_json()
        assert data["message"] == "Organisation post attempted - check import-error log for issues"


def test_post_organisation_data_no_json(client, app_context, monkeypatch):
    monkeypatch.setattr("arctic_office_projects_api.validate_token", lambda token: {"sub": "test-user"})

    response = client.post(
        "/post-organisation-data",
        json={},
        headers={"Authorization": "Bearer fake_token"}
    )

    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "No JSON body provided"


def test_post_organisation_data_existing(
    client, app_context, monkeypatch
):
    monkeypatch.setattr(
        "arctic_office_projects_api.validate_token",
        lambda token: {"sub": "test-user"}
    )

    existing_organisation = Project_Organisations(
        organisation_id="test-organisation-existing",
        organisation_name="Existing Organisation",
        organisation_ror="https://ror.org/existing"
    )

    db.session.add(existing_organisation)
    db.session.commit()

    payload = {
        "organisation_id": "test-organisation-existing",
        "organisation_name": "Existing Organisation",
        "organisation_ror": "https://ror.org/existing"
    }

    response = client.post(
        "/post-organisation-data",
        json=payload,
        headers={"Authorization": "Bearer fake_token"}
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["message"] == (
        "Organisation already imported: Existing Organisation"
    )


def test_post_person_data_success(client, app_context, monkeypatch):
    # Patch authentication
    monkeypatch.setattr("arctic_office_projects_api.validate_token", lambda token: {"sub": "test-user"})

    payload = {
        "name": "Alice Example",
        "gtr_person": "person123",
        "orcid": "0000-0001-2345-6789"
    }

    with patch("arctic_office_projects_api.db.session.add") as mock_add, \
         patch("arctic_office_projects_api.db.session.commit") as mock_commit:

        response = client.post(
            "/post-person-data",
            json=payload,
            headers={"Authorization": "Bearer fake_token"}
        )

        # Ensure DB methods were called
        mock_add.assert_called_once()
        mock_commit.assert_called_once()

        # Assert response
        assert response.status_code == 201
        data = response.get_json()
        assert data["message"] == "Person post attempted - check import-error log for issues"


def test_post_person_data_no_json(client, app_context, monkeypatch):
    monkeypatch.setattr("arctic_office_projects_api.validate_token", lambda token: {"sub": "test-user"})

    response = client.post(
        "/post-person-data",
        json={},
        headers={"Authorization": "Bearer fake_token"}
    )

    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "No JSON body provided"


def test_post_person_data_existing(
    client, app_context, monkeypatch
):
    monkeypatch.setattr(
        "arctic_office_projects_api.validate_token",
        lambda token: {"sub": "test-user"}
    )

    existing_person = Project_People(
        name="Existing Person",
        gtr_person="FFFFFFFF-FFFF-4FFF-8FFF-FFFFFFFFFFF0",
        orcid="https://orcid.org/0000-0002-0143-9999"
    )

    db.session.add(existing_person)
    db.session.commit()

    payload = {
        "name": "Existing Person",
        "gtr_person": "FFFFFFFF-FFFF-4FFF-8FFF-FFFFFFFFFFF0",
        "orcid": "https://orcid.org/0000-0002-0143-9999"
    }

    response = client.post(
        "/post-person-data",
        json=payload,
        headers={"Authorization": "Bearer fake_token"}
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["message"] == (
        "Person already imported: Existing Person"
    )


def test_post_subject_data_success(client, app_context, monkeypatch):
    # Patch authentication
    monkeypatch.setattr("arctic_office_projects_api.validate_token", lambda token: {"sub": "test-user"})

    payload = {
        "subject_text": "Atmosphere",
        "gcmd_link_code": "T1"
    }

    with patch("arctic_office_projects_api.db.session.add") as mock_add, \
         patch("arctic_office_projects_api.db.session.commit") as mock_commit:

        response = client.post(
            "/post-subject-data",
            json=payload,
            headers={"Authorization": "Bearer fake_token"}
        )

        # Ensure DB methods were called
        mock_add.assert_called_once()
        mock_commit.assert_called_once()

        # Assert response
        assert response.status_code == 201
        data = response.get_json()
        assert data["message"] == "Subject post attempted - check import-error log for issues"


def test_post_subject_data_no_json(client, app_context, monkeypatch):
    monkeypatch.setattr("arctic_office_projects_api.validate_token", lambda token: {"sub": "test-user"})

    response = client.post(
        "/post-subject-data",
        json={},
        headers={"Authorization": "Bearer fake_token"}
    )

    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "No JSON body provided"


def test_post_subject_data_existing(
    client, app_context, monkeypatch
):
    monkeypatch.setattr(
        "arctic_office_projects_api.validate_token",
        lambda token: {"sub": "test-user"}
    )

    existing_subject = Project_Subjects(
        subject_text="Existing Subject",
        gcmd_link_code="test.gcmd/subject/existing"
    )

    db.session.add(existing_subject)
    db.session.commit()

    payload = {
        "subject_text": "Existing Subject",
        "gcmd_link_code": "test.gcmd/subject/existing"
    }

    response = client.post(
        "/post-subject-data",
        json=payload,
        headers={"Authorization": "Bearer fake_token"}
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["message"] == (
        "Subject already imported: test.gcmd/subject/existing"
    )


def test_post_topic_data_success(client, app_context, monkeypatch):
    monkeypatch.setattr(
        "arctic_office_projects_api.validate_token",
        lambda token: {"sub": "test-user"}
    )

    payload = {
        "topic_id": "99999999-9999-9999-9999-999999999999",
        "topic_name": "Water+Quality",
        "gcmd_link_name": "WATER QUALITY",
        "gcmd_link_code": (
            "gcmd.earthdata.nasa.gov/kms/concept/"
            "1ee8a323-f0ba-4a21-b597-50890c527c8e"
        )
    }

    with patch("arctic_office_projects_api.db.session.add") as mock_add, \
         patch("arctic_office_projects_api.db.session.commit") as mock_commit:

        response = client.post(
            "/post-topic-data",
            json=payload,
            headers={"Authorization": "Bearer fake_token"}
        )

        assert response.status_code == 201
        mock_add.assert_called_once()
        mock_commit.assert_called_once()


def test_post_topic_data_no_json(client, app_context, monkeypatch):
    monkeypatch.setattr("arctic_office_projects_api.validate_token", lambda token: {"sub": "test-user"})

    response = client.post(
        "/post-topic-data",
        json={},
        headers={"Authorization": "Bearer fake_token"}
    )

    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "No JSON body provided"


def test_post_topic_data_existing(
    client, app_context, monkeypatch
):
    monkeypatch.setattr(
        "arctic_office_projects_api.validate_token",
        lambda token: {"sub": "test-user"}
    )

    existing_topic = Project_Topics(
        topic_id="FFFFFFFF-FFFF-4FFF-8FFF-FFFFFFFFFFF0",
        topic_name="Existing Topic",
        gcmd_link_name="EXISTING TOPIC",
        gcmd_link_code="test.gcmd/topic/existing"
    )

    db.session.add(existing_topic)
    db.session.commit()

    payload = {
        "topic_id": "FFFFFFFF-FFFF-4FFF-8FFF-FFFFFFFFFFF0",
        "topic_name": "Existing Topic",
        "gcmd_link_name": "EXISTING TOPIC",
        "gcmd_link_code": "test.gcmd/topic/existing"
    }

    response = client.post(
        "/post-topic-data",
        json=payload,
        headers={"Authorization": "Bearer fake_token"}
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["message"] == (
        "Topic already imported: FFFFFFFF-FFFF-4FFF-8FFF-FFFFFFFFFFF0"
    )


def test_post_subject_data_bulk_success(client, app_context, monkeypatch):
    # Patch authentication
    monkeypatch.setattr(
        "arctic_office_projects_api.validate_token",
        lambda token: {"sub": "test-user"}
    )

    payload = [
        {
            "subject_text": "Water Quality",
            "gcmd_link_code": "test.gcmd/subject/001"
        },
        {
            "subject_text": "Climate",
            "gcmd_link_code": "test.gcmd/subject/002"
        }
    ]

    with patch("arctic_office_projects_api.db.session.add") as mock_add, \
         patch("arctic_office_projects_api.db.session.commit") as mock_commit:

        response = client.post(
            "/post-subject-data-bulk",
            json=payload,
            headers={"Authorization": "Bearer fake_token"}
        )

        mock_add.assert_called()
        assert mock_add.call_count == 2
        mock_commit.assert_called_once()

        assert response.status_code == 201

        data = response.get_json()
        assert data["message"] == (
            "Subject posts attempted - check import-error log for issues"
        )
        assert data["added"] == 2
        assert data["skipped"] == 0


def test_post_subject_data_bulk_existing_subjects(
    client, app_context, monkeypatch
):
    monkeypatch.setattr(
        "arctic_office_projects_api.validate_token",
        lambda token: {"sub": "test-user"}
    )

    existing_subject = Project_Subjects(
        subject_text="Existing Subject",
        gcmd_link_code="test.gcmd/subject/existing"
    )

    db.session.add(existing_subject)
    db.session.commit()

    payload = [
        {
            "subject_text": "Existing Subject",
            "gcmd_link_code": "test.gcmd/subject/existing"
        },
        {
            "subject_text": "New Subject",
            "gcmd_link_code": "test.gcmd/subject/new"
        },
        {
            "subject_text": "Another New Subject",
            "gcmd_link_code": "test.gcmd/subject/new2"
        }
    ]

    with patch("arctic_office_projects_api.db.session.add") as mock_add, \
         patch("arctic_office_projects_api.db.session.commit") as mock_commit:

        response = client.post(
            "/post-subject-data-bulk",
            json=payload,
            headers={"Authorization": "Bearer fake_token"}
        )

        assert response.status_code == 201

        data = response.get_json()
        assert data["added"] == 2
        assert data["skipped"] == 1

        assert mock_add.call_count == 2
        mock_commit.assert_called_once()


def test_post_subject_data_bulk_no_data(
    client, app_context, monkeypatch
):
    monkeypatch.setattr(
        "arctic_office_projects_api.validate_token",
        lambda token: {"sub": "test-user"}
    )

    response = client.post(
        "/post-subject-data-bulk",
        json={},
        headers={"Authorization": "Bearer fake_token"}
    )

    assert response.status_code == 400

    data = response.get_json()
    assert data["error"] == "No JSON body provided"


def test_post_organisation_data_bulk_success(client, app_context, monkeypatch):
    # Patch authentication
    monkeypatch.setattr(
        "arctic_office_projects_api.validate_token",
        lambda token: {"sub": "test-user"}
    )

    payload = [
        {
            "organisation_id": "test-organisation-001",
            "organisation_name": "Test Organisation One",
            "organisation_ror": "https://ror.org/test001"
        },
        {
            "organisation_id": "test-organisation-002",
            "organisation_name": "Test Organisation Two",
            "organisation_ror": "https://ror.org/test002"
        }
    ]

    with patch("arctic_office_projects_api.db.session.add") as mock_add, \
         patch("arctic_office_projects_api.db.session.commit") as mock_commit:

        response = client.post(
            "/post-organisation-data-bulk",
            json=payload,
            headers={"Authorization": "Bearer fake_token"}
        )

        assert response.status_code == 201

        data = response.get_json()
        assert data["message"] == (
            "Organisation posts attempted - check import-error log for issues"
        )
        assert data["added"] == 2
        assert data["skipped"] == 0

        assert mock_add.call_count == 2
        mock_commit.assert_called_once()


def test_post_organisation_data_bulk_existing_organisations(
    client, app_context, monkeypatch
):
    monkeypatch.setattr(
        "arctic_office_projects_api.validate_token",
        lambda token: {"sub": "test-user"}
    )

    existing_organisation = Project_Organisations(
        organisation_id="test-organisation-existing",
        organisation_name="Existing Organisation",
        organisation_ror="https://ror.org/existing"
    )

    db.session.add(existing_organisation)
    db.session.commit()

    payload = [
        {
            "organisation_id": "test-organisation-existing",
            "organisation_name": "Existing Organisation",
            "organisation_ror": "https://ror.org/existing"
        },
        {
            "organisation_id": "test-organisation-new-001",
            "organisation_name": "New Organisation One",
            "organisation_ror": "https://ror.org/new001"
        },
        {
            "organisation_id": "test-organisation-new-002",
            "organisation_name": "New Organisation Two",
            "organisation_ror": "https://ror.org/new002"
        }
    ]

    with patch("arctic_office_projects_api.db.session.add") as mock_add, \
         patch("arctic_office_projects_api.db.session.commit") as mock_commit:

        response = client.post(
            "/post-organisation-data-bulk",
            json=payload,
            headers={"Authorization": "Bearer fake_token"}
        )

        assert response.status_code == 201

        data = response.get_json()
        assert data["added"] == 2
        assert data["skipped"] == 1

        assert mock_add.call_count == 2
        mock_commit.assert_called_once()


def test_post_organisation_data_bulk_no_data(
    client, app_context, monkeypatch
):
    monkeypatch.setattr(
        "arctic_office_projects_api.validate_token",
        lambda token: {"sub": "test-user"}
    )

    response = client.post(
        "/post-organisation-data-bulk",
        json={},
        headers={"Authorization": "Bearer fake_token"}
    )

    assert response.status_code == 400

    data = response.get_json()
    assert data["error"] == "No JSON body provided"


def test_post_person_data_bulk_success(client, app_context, monkeypatch):
    # Patch authentication
    monkeypatch.setattr(
        "arctic_office_projects_api.validate_token",
        lambda token: {"sub": "test-user"}
    )

    payload = [
        {
            "name": "test-person-001",
            "gtr_person": "8B101538-BE28-41A2-AF8A-FFFFFFFFFFF1",
            "orcid": "https://orcid.org/0000-0002-0143-1111"
        },
        {
            "name": "test-person-002",
            "gtr_person": "8B101538-BE28-41A2-AF8A-FFFFFFFFFFF2",
            "orcid": "https://orcid.org/0000-0002-0143-2222"
        }
    ]

    with patch("arctic_office_projects_api.db.session.add") as mock_add, \
         patch("arctic_office_projects_api.db.session.commit") as mock_commit:

        response = client.post(
            "/post-person-data-bulk",
            json=payload,
            headers={"Authorization": "Bearer fake_token"}
        )

        assert response.status_code == 201

        data = response.get_json()
        assert data["message"] == (
            "Person posts attempted - check import-error log for issues"
        )
        assert data["added"] == 2
        assert data["skipped"] == 0

        assert mock_add.call_count == 2
        mock_commit.assert_called_once()


def test_post_person_data_bulk_existing_person(
    client, app_context, monkeypatch
):
    monkeypatch.setattr(
        "arctic_office_projects_api.validate_token",
        lambda token: {"sub": "test-user"}
    )

    existing_organisation = Project_People(
        name="test-person-existing",
        gtr_person="8B101538-BE28-41A2-AF8A-FFFFFFFFFFF3",
        orcid="https://orcid.org/0000-0002-0143-3333"
    )

    db.session.add(existing_organisation)
    db.session.commit()

    payload = [
        {
            "name": "test-person-existing",
            "gtr_person": "8B101538-BE28-41A2-AF8A-FFFFFFFFFFF3",
            "orcid": "https://orcid.org/0000-0002-0143-3333"
        },
        {
            "name": "test-person-002",
            "gtr_person": "8B101538-BE28-41A2-AF8A-FFFFFFFFFFF4",
            "orcid": "https://orcid.org/0000-0002-0143-4444"
        },
                {
            "name": "test-person-003",
            "gtr_person": "8B101538-BE28-41A2-AF8A-FFFFFFFFFFF5",
            "orcid": "https://orcid.org/0000-0002-0143-5555"
        }
    ]

    with patch("arctic_office_projects_api.db.session.add") as mock_add, \
         patch("arctic_office_projects_api.db.session.commit") as mock_commit:

        response = client.post(
            "/post-person-data-bulk",
            json=payload,
            headers={"Authorization": "Bearer fake_token"}
        )

        assert response.status_code == 201

        data = response.get_json()
        assert data["added"] == 2
        assert data["skipped"] == 1

        assert mock_add.call_count == 2
        mock_commit.assert_called_once()


def test_post_person_data_bulk_invalid_json(
    client, app_context, monkeypatch
):
    monkeypatch.setattr(
        "arctic_office_projects_api.validate_token",
        lambda token: {"sub": "test-user"}
    )

    response = client.post(
        "/post-person-data-bulk",
        json={
            "name": "Test Person",
            "gtr_person": "test-person-001",
            "orcid": "https://orcid.org/0000-0002-0143-1111"
        },
        headers={"Authorization": "Bearer fake_token"}
    )

    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "JSON body must be a list of people"


def test_post_person_data_bulk_no_data(
    client, app_context, monkeypatch
):
    monkeypatch.setattr(
        "arctic_office_projects_api.validate_token",
        lambda token: {"sub": "test-user"}
    )

    response = client.post(
        "/post-person-data-bulk",
        json={},
        headers={"Authorization": "Bearer fake_token"}
    )

    assert response.status_code == 400

    data = response.get_json()
    assert data["error"] == "No JSON body provided"


def test_post_topic_data_bulk_success(client, app_context, monkeypatch):
    # Patch authentication
    monkeypatch.setattr(
        "arctic_office_projects_api.validate_token",
        lambda token: {"sub": "test-user"}
    )

    payload = [
        {
            "topic_id": "FFFFFFFF-FFFF-4FFF-8FFF-FFFFFFFFFFF1",
            "topic_name": "test-topic-001",
            "gcmd_link_name": "TEST TOPIC 001",
            "gcmd_link_code": "test.gcmd/topic/001"
        },
        {
            "topic_id": "FFFFFFFF-FFFF-4FFF-8FFF-FFFFFFFFFFF2",
            "topic_name": "test-topic-002",
            "gcmd_link_name": "TEST TOPIC 002",
            "gcmd_link_code": "test.gcmd/topic/002"
        }
    ]

    with patch("arctic_office_projects_api.db.session.add") as mock_add, \
         patch("arctic_office_projects_api.db.session.commit") as mock_commit:

        response = client.post(
            "/post-topic-data-bulk",
            json=payload,
            headers={"Authorization": "Bearer fake_token"}
        )

        assert response.status_code == 201

        data = response.get_json()
        assert data["message"] == (
            "Topic posts attempted - check import-error log for issues"
        )
        assert data["added"] == 2
        assert data["skipped"] == 0

        assert mock_add.call_count == 2
        mock_commit.assert_called_once()


def test_post_topic_data_bulk_existing_topics(
    client, app_context, monkeypatch
):
    monkeypatch.setattr(
        "arctic_office_projects_api.validate_token",
        lambda token: {"sub": "test-user"}
    )

    existing_topic = Project_Topics(
        topic_id="FFFFFFFF-FFFF-4FFF-8FFF-FFFFFFFFFFF0",
        topic_name="Existing Topic",
        gcmd_link_name="EXISTING TOPIC",
        gcmd_link_code="test.gcmd/topic/existing"
    )

    db.session.add(existing_topic)
    db.session.commit()

    payload = [
        {
            "topic_id": "FFFFFFFF-FFFF-4FFF-8FFF-FFFFFFFFFFF0",
            "topic_name": "Existing Topic",
            "gcmd_link_name": "EXISTING TOPIC",
            "gcmd_link_code": "test.gcmd/topic/existing"
        },
        {
            "topic_id": "FFFFFFFF-FFFF-4FFF-8FFF-FFFFFFFFFFF3",
            "topic_name": "New Topic One",
            "gcmd_link_name": "NEW TOPIC ONE",
            "gcmd_link_code": "test.gcmd/topic/new1"
        },
        {
            "topic_id": "FFFFFFFF-FFFF-4FFF-8FFF-FFFFFFFFFFF4",
            "topic_name": "New Topic Two",
            "gcmd_link_name": "NEW TOPIC TWO",
            "gcmd_link_code": "test.gcmd/topic/new2"
        }
    ]

    with patch("arctic_office_projects_api.db.session.add") as mock_add, \
         patch("arctic_office_projects_api.db.session.commit") as mock_commit:

        response = client.post(
            "/post-topic-data-bulk",
            json=payload,
            headers={"Authorization": "Bearer fake_token"}
        )

        assert response.status_code == 201

        data = response.get_json()
        assert data["message"] == (
            "Topic posts attempted - check import-error log for issues"
        )
        assert data["added"] == 2
        assert data["skipped"] == 1

        assert mock_add.call_count == 2
        mock_commit.assert_called_once()


def test_post_topic_data_bulk_no_data(
    client, app_context, monkeypatch
):
    monkeypatch.setattr(
        "arctic_office_projects_api.validate_token",
        lambda token: {"sub": "test-user"}
    )

    response = client.post(
        "/post-topic-data-bulk",
        json={},
        headers={"Authorization": "Bearer fake_token"}
    )

    assert response.status_code == 400

    data = response.get_json()
    assert data["error"] == "No JSON body provided"
