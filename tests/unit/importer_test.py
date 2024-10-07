import pytest
from unittest.mock import patch, mock_open
from sqlalchemy.exc import SQLAlchemyError
from arctic_office_projects_api.importers import (
    import_category_terms_from_file_interactively,
    import_organisations_from_file_interactively,
    _generate_category_term_ltree_path,
)
from jsonschema import ValidationError


@pytest.fixture
def mock_db_session():
    """Fixture to mock the db session manually with patch."""
    with patch('arctic_office_projects_api.db.session') as mock_session:
        # Mock any database-specific behavior
        mock_session.query.return_value.scalar.return_value = False
        yield mock_session


@pytest.fixture
def category_data():
    """Sample category data for testing."""
    return {
        "schemes": [{"namespace": "namespace1", "title": "Scheme1", "root-concepts": []}],
        "terms": [{"subject": "subject1", "pref-label": "Term1", "path": {"id": "root"}, "scheme": "namespace1"}],
    }

@pytest.fixture
def invalid_category_data():
    """Sample category data for testing."""
    return {
        "terms": [{"subject": "subject1", "pref-label": "Term1", "path": {"id": "root"}, "scheme": "namespace1"}],
    }


@pytest.fixture
def category_terms_data():
    """Sample category terms data for testing."""
    return {
        "schemes": [
            {
                "namespace": "test_namespace",
                "title": "Test Scheme",
                "root-concepts": ["root_concept_1"],
                "acronym": "TS",
                "description": "A test scheme",
            }
        ],
        "terms": [
            {
                "subject": "term_subject",
                "pref-label": "Test Term",
                "path": {"parent1": "http://example.com/parent1", "parent2": "http://example.com/parent2"},
                "scheme": "test_namespace",
            }
        ],
    }

@pytest.fixture
def organisations_data():
    """Sample organisations data for testing."""
    return {
        "organisations": [
            {
                "ror-identifier": "org-1",
                "name": "Organisation 1",
                "acronym": "ORG1",
                "website": "http://example.com",
                "logo-url": "http://example.com/logo.png",
                "version": "1.0",
            }
        ]
    }


@patch('builtins.open', new_callable=mock_open, create=True)
@patch('simplejson.load')
@patch('jsonschema.validate')
def test_import_category_terms_happy_path(mock_validate, mock_load, mock_open, mock_db_session, category_data):
    """Test the successful import of category terms."""
    
    # Prepare mock load to return valid data
    mock_load.side_effect = [
        {"type": "object", "properties": {}},  # First call: schema
        category_data  # Second call: category_data
    ]

    categories_file_path = "test_categories.json"  # Example path for the test

    # Call the function to test
    import_category_terms_from_file_interactively(categories_file_path)

    # Check that the schema validation was called
    # mock_validate.assert_called_once()

    # Verify database operations
    assert mock_db_session.add.called  # Check if something was added to the session
    assert mock_db_session.commit.called  # Check if commit was called
    assert mock_db_session.rollback.call_count == 0  # Ensure rollback was not called


@patch('builtins.open', new_callable=mock_open, create=True)
@patch('simplejson.load')
@patch('jsonschema.validate')
def test_import_organisations_happy_path(mock_validate, mock_load, mock_open, mock_db_session, organisations_data):
    """Test the successful import of organisations."""

    # Prepare mock load to return valid data
    mock_load.side_effect = [
        {"type": "object", "properties": {}},  # First call: schema
        organisations_data  # Second call: organisations_data
    ]    

    organisations_file_path = "test_organisations.json"  # Example path for the test

    # Call the function to test
    import_organisations_from_file_interactively(organisations_file_path)

    # Check that the schema validation was called
    # mock_validate.assert_called_once()

    # Verify database operations
    assert mock_db_session.add.called  # Check if something was added to the session
    assert mock_db_session.commit.called  # Check if commit was called
    assert mock_db_session.rollback.call_count == 0  # Ensure rollback was not called


@patch('builtins.open')
@patch('simplejson.load')
@patch('jsonschema.validate')
def test_import_category_terms_file_not_found(mock_validate, mock_load, mock_open, mock_db_session):
    """Test category term import when the file is not found."""
    mock_open.side_effect = FileNotFoundError  # Simulate file not found error
    categories_file_path = "non_existent_file.json"

    with pytest.raises(FileNotFoundError):
        import_category_terms_from_file_interactively(categories_file_path)

    assert mock_db_session.rollback.called
    assert mock_db_session.flush.called


@patch('builtins.open', new_callable=mock_open, create=True)
@patch('simplejson.load')
@patch('jsonschema.validate', side_effect=ValidationError("Invalid JSON"))
def test_import_category_terms_invalid_schema(mock_validate, mock_load, mock_open, mock_db_session, invalid_category_data):
    """Test schema validation failure during category import."""
    # Mock the load to return the invalid category data
    mock_load.side_effect = [
        {"type": "object", "properties": {}},  # First call: schema
        invalid_category_data  # Second call: invalid category data
    ]
    
    categories_file_path = "test_categories.json"

    with pytest.raises(KeyError) as excinfo:
        import_category_terms_from_file_interactively(categories_file_path)

    assert "schemes" in str(excinfo.value)  # Ensure the KeyError is due to missing 'schemes'



@patch('builtins.open', new_callable=mock_open, create=True)
@patch('simplejson.load')
@patch('jsonschema.validate')
def test_import_category_terms_db_error(mock_validate, mock_load, mock_open, mock_db_session, category_data):
    """Test database error during category import."""
    mock_load.side_effect = [
        {"type": "object", "properties": {}},  # First call: schema
        category_data  # Second call: categories_data
    ]

    mock_db_session.add.side_effect = SQLAlchemyError("DB error")  # Simulate a DB error
    categories_file_path = "test_categories.json"

    with pytest.raises(SQLAlchemyError):
        import_category_terms_from_file_interactively(categories_file_path)

    assert mock_db_session.rollback.called  # Ensure rollback is called
    assert mock_db_session.flush.called  # Ensure flush is called


def test_generate_category_term_ltree_path():
    """Test generating an ltree path for category terms."""
    path_elements = {"0": "http://example.com/12", "1": "http://example.com/1"}
    expected_ltree = "http_example_com_12.http_example_com_1"

    result = _generate_category_term_ltree_path(path_elements)
    assert str(result) == expected_ltree


def test_generate_category_term_ltree_path_empty():
    """Test handling empty path elements in _generate_category_term_ltree_path."""
    path_elements = {}

    with pytest.raises(ValueError, match="Path for category cannot be empty"):
        _generate_category_term_ltree_path(path_elements)
