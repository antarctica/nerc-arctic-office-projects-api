import os
import sys
import unittest

from flask.cli import AppGroup
from flask_migrate import Migrate

from arctic_office_projects_api import create_app, db
from arctic_office_projects_api.models import Project, Person, Participant, Grant, Allocation, Organisation, \
    CategoryScheme, CategoryTerm, Categorisation
from arctic_office_projects_api.seeding import seed_predictable_test_resources, seed_random_test_resources

app = create_app(os.getenv('FLASK_ENV') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(
        db=db,
        Project=Project,
        Person=Person,
        Participant=Participant,
        Grant=Grant,
        Allocation=Allocation,
        Organisation=Organisation,
        CategoryScheme=CategoryScheme,
        CategoryTerm=CategoryTerm,
        Categorisation=Categorisation
    )


@app.cli.command()
def test():
    """Run integration tests."""
    tests = unittest.TestLoader().discover(os.path.join(os.path.dirname(__file__), 'tests'))
    tests_runner = unittest.TextTestRunner(verbosity=2)
    return sys.exit(not tests_runner.run(tests).wasSuccessful())


seeding_cli_group = AppGroup('seed', help='Perform database seeding')
app.cli.add_command(seeding_cli_group)


@seeding_cli_group.command('predictable')
def seed_predictable_mock_projects():
    """Seed database with predictable mock projects."""
    seed_predictable_test_resources()
    print("Seeded predictable mock resources")


@seeding_cli_group.command('random')
def seed_random_mock_projects():
    """Seed database with 100 random mock projects."""
    seed_random_test_resources()
    print("Seeded random mock resources")


if 'PYCHARM_HOSTED' in os.environ:
    # Exempting Bandit security issue (binding to all network interfaces)
    #
    # All interfaces option used because the network available within the container can vary across providers
    # This is only used when debugging with PyCharm. A standalone web server is used in production.
    app.run(host='0.0.0.0', port=9000, debug=True, use_debugger=False, use_reloader=False)  # nosec
