import os
import sys
import unittest

# noinspection PyPackageRequirements
from click import option, IntRange
from flask_migrate import Migrate

from arctic_office_projects_api import create_app, db
from arctic_office_projects_api.models import Project, Person, Participant, Grant, Allocation

app = create_app(os.getenv('FLASK_ENV') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Project=Project, Person=Person)


@app.cli.command()
def test():
    """Run integration tests."""
    tests = unittest.TestLoader().discover(os.path.join(os.path.dirname(__file__), 'tests'))
    tests_runner = unittest.TextTestRunner(verbosity=2)
    return sys.exit(not tests_runner.run(tests).wasSuccessful())


@app.cli.command()
@option('--count', type=IntRange(1, 10000), default=1, help='Target number of fake Project resources to add')
def seed(count):
    """Seed database with mock data."""
    try:
        Grant.seed(quantity=count)
        project = Project()
        project.seed(quantity=count)
        Person.seed(quantity=count)
        Participant.seed(quantity=count)
        Allocation.seed(quantity=count)

        db.session.commit()
        print("Seeding OK")
    except Exception as e:
        db.session.rollback()
        # reset added, but non-committed, entities
        db.session.flush()
        raise e


if 'PYCHARM_HOSTED' in os.environ:
    # Exempting Bandit security issue (binding to all network interfaces)
    #
    # All interfaces option used because the network available within the container can vary across providers
    # This is only used when debugging with PyCharm. A standalone web server is used in production.
    app.run(host='0.0.0.0', port=9000, debug=True, use_debugger=False, use_reloader=False)  # nosec
