import os
import sys
import unittest

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
def test():
    """Run integration tests."""
    tests = unittest.TestLoader().discover(os.path.join(os.path.dirname(__file__), 'tests'))
    tests_runner = unittest.TextTestRunner(verbosity=2)
    return sys.exit(not tests_runner.run(tests).wasSuccessful())


if 'PYCHARM_HOSTED' in os.environ:
    # Exempting Bandit security issue (binding to all network interfaces)
    #
    # All interfaces option used because the network available within the container can vary across providers
    # This is only used when debugging with PyCharm. A standalone web server is used in production.
    app.run(host='0.0.0.0', port=9000, debug=True, use_debugger=False, use_reloader=False)  # nosec
