import pytest
from flask import Flask
from unittest.mock import patch

# Import your CLI groups and commands
from arctic_office_projects_api.commands import (
    seeding_cli_group,
    importing_cli_group
)

# Create a test app factory
@pytest.fixture
def app():
    app = Flask(__name__)
    app.cli.add_command(seeding_cli_group)
    app.cli.add_command(importing_cli_group)
    return app


# Test seed_predictable_mock_projects
@patch("arctic_office_projects_api.commands.seed_predictable_test_resources")
def test_seed_predictable_mock_projects(mock_seed_predictable, app):
    runner = app.test_cli_runner()  # Use app's CLI runner
    with app.app_context():  # Push the app context
        result = runner.invoke(args=["seed", "predictable"])

    # Check if the seed_predictable_test_resources function was called
    mock_seed_predictable.assert_called_once()

    # Check the CLI output
    assert result.exit_code == 0
    assert "Seeded predictable mock resources" in result.output


# Test seed_random_mock_projects
@patch("arctic_office_projects_api.commands.seed_random_test_resources")
def test_seed_random_mock_projects(mock_seed_random, app):
    runner = app.test_cli_runner()  # Use app's CLI runner
    with app.app_context():  # Push the app context
        result = runner.invoke(args=["seed", "random"])

    # Check if the seed_random_test_resources function was called
    mock_seed_random.assert_called_once()

    # Check the CLI output
    assert result.exit_code == 0
    assert "Seeded random mock resources" in result.output


# Test import_categories_from_file
@patch("arctic_office_projects_api.commands.import_category_terms_from_file_interactively")
def test_import_categories_from_file(mock_import_categories, app):
    runner = app.test_cli_runner()  # Use app's CLI runner
    with app.app_context():  # Push the app context

        # Create a mock file for the file path argument
        with runner.isolated_filesystem():
            with open("categories.json", "w") as f:
                f.write("[]")

            result = runner.invoke(args=["import", "categories", "categories.json"])

            # Check if the import_category_terms_from_file_interactively function was called
            mock_import_categories.assert_called_once_with(categories_file_path="categories.json")

            # Check the CLI output
            assert result.exit_code == 0


# Test import_organisations_from_file
@patch("arctic_office_projects_api.commands.import_organisations_from_file_interactively")
def test_import_organisations_from_file(mock_import_organisations, app):
    runner = app.test_cli_runner()  # Use app's CLI runner
    with app.app_context():  # Push the app context

        # Create a mock file for the file path argument
        with runner.isolated_filesystem():
            with open("organisations.json", "w") as f:
                f.write("[]")

            result = runner.invoke(args=["import", "organisations", "organisations.json"])

            # Check if the import_organisations_from_file_interactively function was called
            mock_import_organisations.assert_called_once_with(organisations_file_path="organisations.json")

            # Check the CLI output
            assert result.exit_code == 0


# Test import_grant_from_provider
@patch("arctic_office_projects_api.commands.import_gateway_to_research_grant_interactively")
def test_import_grant_from_provider(mock_import_grant, app):
    runner = app.test_cli_runner()  # Use app's CLI runner
    with app.app_context():  # Push the app context

        result = runner.invoke(args=["import", "grant", "gtr", "GRANT123", "1"])

        # Check if the import_gateway_to_research_grant_interactively function was called
        mock_import_grant.assert_called_once_with("GRANT123", 1)

        # Check the CLI output
        assert result.exit_code == 0
