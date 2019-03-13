# noinspection PyPackageRequirements
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
# noinspection PyPackageRequirements
from werkzeug.exceptions import NotFound, Conflict
from flask import Blueprint, jsonify, request, current_app as app

from arctic_office_projects_api.schemas import ProjectSchema, PersonSchema
from arctic_office_projects_api.models import Project, Person

main = Blueprint('main', __name__)


@main.route("/")
def index():
    """
    Returns a simple welcome message
    """

    payload = {
        'meta': {
            'summary': 'xxx'
        }
    }

    return jsonify(payload)


@main.route('/projects')
def projects_list():
    """
    Returns details for all Project resources

    The response is paginated.
    """
    page = request.args.get('page', type=int)
    if page is None:
        page = 1

    projects = Project.query.paginate(page=page, per_page=app.config['APP_PAGE_SIZE'])
    payload = ProjectSchema(many=True, paginate=True).dump(projects)

    return jsonify(payload.data)


@main.route('/projects/<project_id>')
def projects_detail(project_id: str):
    """
    Returns details for a specific Project resource, specified by its Neutral ID

    :type project_id: str
    :param project_id: Neutral ID of a Project resource
    """
    try:
        project = Project.query.filter_by(neutral_id=project_id).one()
        return jsonify(payload.data)
    except NoResultFound:
        raise NotFound()
    payload = ProjectSchema().dump(project)
    except MultipleResultsFound:
        raise Conflict()

    return jsonify(payload.data)


@main.route('/projects/<project_id>/relationships/people')
def projects_people_relationship(project_id: str):
    pass


@main.route('/projects/<project_id>/people')
def projects_people(project_id: str):
    pass


@main.route('/people')
def people_list():
    """
    Returns details for all People resources

    The response is paginated.
    """
    page = request.args.get('page', type=int)
    if page is None:
        page = 1

    people = Person.query.paginate(page=page, per_page=app.config['APP_PAGE_SIZE'])
    payload = PersonSchema(many=True, paginate=True).dump(people)

    return jsonify(payload.data)


@main.route('/people/<person_id>')
def people_detail(person_id: str):
    """
    Returns details for a specific Person resource, specified by its Neutral ID

    :type person_id: str
    :param person_id: Neutral ID of a Person resource
    """
    person = Person.query.filter_by(neutral_id=person_id).first()
    if person is None:
        raise NotFound()
    payload = ProjectSchema().dump(person)

    return jsonify(payload.data)
