import os
import sys
import unittest
import xmlrunner

# noinspection PyPackageRequirements
from click import option, Choice
from flask_migrate import Migrate

from arctic_office_projects_api import create_app, db
from arctic_office_projects_api.models import Project, Person, Participant, Grant, Allocation, Organisation, \
    CategoryScheme, CategoryTerm, Categorisation

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
@option('--test-runner', type=Choice(['text', 'junit']))
def test(test_runner: str = 'text'):
    """Run integration tests."""
    tests = unittest.TestLoader().discover(os.path.join(os.path.dirname(__file__), 'tests'))

    if test_runner == 'text':
        tests_runner = unittest.TextTestRunner(verbosity=2)
        return sys.exit(not tests_runner.run(tests).wasSuccessful())
    elif test_runner == 'junit':
        with open('test-results.xml', 'wb') as output:
            tests_runner = xmlrunner.XMLTestRunner(output=output)
            return sys.exit(not tests_runner.run(tests).wasSuccessful())

    return RuntimeError('Unknown Python unit test runner type')


if 'PYCHARM_HOSTED' in os.environ:
    # Exempting Bandit security issue (binding to all network interfaces)
    #
    # All interfaces option used because the network available within the container can vary across providers
    # This is only used when debugging with PyCharm. A standalone web server is used in production.
    app.run(host='0.0.0.0', port=9000, debug=True, use_debugger=False, use_reloader=False)  # nosec
