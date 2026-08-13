import os

# noinspection PyPackageRequirements
from flask_migrate import Migrate

from arctic_office_projects_api import create_app, db
from arctic_office_projects_api.models import (
    Project,
    Person,
    Participant,
    Grant,
    Allocation,
    Organisation,
    CategoryScheme,
    CategoryTerm,
    Categorisation
)

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
