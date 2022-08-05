# noinspection PyPackageRequirements
from click import argument, Path, Choice, echo, style
from flask.cli import AppGroup

from arctic_office_projects_api.importers import import_category_terms_from_file_interactively, \
    import_organisations_from_file_interactively
from arctic_office_projects_api.importers.gtr import import_gateway_to_research_grant_interactively
from arctic_office_projects_api.seeding import seed_predictable_test_resources, seed_random_test_resources


seeding_cli_group = AppGroup('seed', help='Perform database seeding.')


@seeding_cli_group.command('predictable')
def seed_predictable_mock_projects():
    """Seed database with predictable mock projects."""
    seed_predictable_test_resources()
    echo(style("Seeded predictable mock resources", fg='green'))


@seeding_cli_group.command('random')
def seed_random_mock_projects():
    """Seed database with 100 random mock projects."""
    seed_random_test_resources()
    echo(style("Seeded random mock resources", fg='green'))


importing_cli_group = AppGroup('import', help='Import data.')


@importing_cli_group.command('categories')
@argument('file_path', type=Path(exists=True))
def import_categories_from_file(file_path):
    """Import research categories from a JSON file"""
    import_category_terms_from_file_interactively(categories_file_path=file_path)


@importing_cli_group.command('organisations')
@argument('file_path', type=Path(exists=True))
def import_organisations_from_file(file_path):
    """Import organisations from a JSON file"""
    import_organisations_from_file_interactively(organisations_file_path=file_path)


@importing_cli_group.command('grant')
@argument('grant_provider', type=Choice(['gtr']))
@argument('grant_reference')
@argument('lead_project', default=False)
def import_grant_from_provider(grant_provider, grant_reference, lead_project):
    """Import a research grant from a provider"""
    if grant_provider == 'gtr':
        import_gateway_to_research_grant_interactively(grant_reference, lead_project)


