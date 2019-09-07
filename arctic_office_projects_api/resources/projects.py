# noinspection PyPackageRequirements
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
# noinspection PyPackageRequirements
from werkzeug.exceptions import NotFound, UnprocessableEntity
from flask import Blueprint, jsonify, request, current_app as app

from arctic_office_projects_api import auth
from arctic_office_projects_api.schemas import ProjectSchema
from arctic_office_projects_api.models import Project

projects = Blueprint('projects', __name__)


@projects.route('/projects')
@auth()
def projects_list():
    """
    Returns all Project resources

    The response is paginated.
    """
    page = request.args.get('page', type=int)
    if page is None:
        page = 1

    projects = Project.query.paginate(page=page, per_page=app.config['APP_PAGE_SIZE'])
    payload = ProjectSchema(many=True, paginate=True, include_data=(
        'participants',
        'participants.person',
        'participants.person.organisation',
        'allocations',
        'allocations.grant',
        'allocations.grant.funder',
        'categorisations',
        'categorisations.category',
        'categorisations.category.category_scheme',
        'categorisations.category.parent_category'
    )).dump(projects)

    return jsonify(payload)


@projects.route('/projects/<project_id>')
@auth()
def projects_detail(project_id: str):
    """
    Returns a specific Project resource, specified by its Neutral ID

    :type project_id: str
    :param project_id: neutral ID of a Project resource
    """
    try:
        project = Project.query.filter_by(neutral_id=project_id).one()
        payload = ProjectSchema(include_data=(
            'participants',
            'participants.person',
            'participants.person.organisation',
            'allocations',
            'allocations.grant',
            'allocations.grant.funder',
            'categorisations',
            'categorisations.category',
            'categorisations.category.category_scheme',
            'categorisations.category.parent_category'
        )).dump(project)
        return jsonify(payload)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()


@projects.route('/projects/<project_id>/relationships/participants')
@auth()
def projects_relationship_participants(project_id: str):
    """
    Returns Participant resource linkages associated with a specific Project resource, specified by its Neutral ID

    :type project_id: str
    :param project_id: neutral ID of a Project resource
    """
    try:
        project = Project.query.filter_by(neutral_id=project_id).one()
        payload = ProjectSchema(resource_linkage='participants').dump(project)
        return jsonify(payload)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()


@projects.route('/projects/<project_id>/relationships/allocations')
@auth()
def projects_relationship_allocations(project_id: str):
    """
    Returns Allocation resource linkages associated with a specific Project resource, specified by its Neutral ID

    :type project_id: str
    :param project_id: neutral ID of a Project resource
    """
    try:
        project = Project.query.filter_by(neutral_id=project_id).one()
        payload = ProjectSchema(resource_linkage='allocations').dump(project)
        return jsonify(payload)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()


@projects.route('/projects/<project_id>/participants')
@auth()
def projects_participants(project_id: str):
    """
    Returns Participant resources associated with a specific Project resource, specified by its Neutral ID

    :type project_id: str
    :param project_id: neutral ID of a Project resource
    """
    try:
        project = Project.query.filter_by(neutral_id=project_id).one()
        payload = ProjectSchema(related_resource='participants', many_related=True).dump(project)
        return jsonify(payload)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()


@projects.route('/projects/<project_id>/allocations')
@auth()
def projects_allocations(project_id: str):
    """
    Returns Allocation resources associated with a specific Project resource, specified by its Neutral ID

    :type project_id: str
    :param project_id: neutral ID of a Project resource
    """
    try:
        project = Project.query.filter_by(neutral_id=project_id).one()
        payload = ProjectSchema(related_resource='allocations', many_related=True).dump(project)
        return jsonify(payload)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()


@projects.route('/projects/<project_id>/relationships/categorisations')
@auth()
def projects_relationship_categorisations(project_id: str):
    """
    Returns Categorisation resource linkages associated with a specific Project resource, specified by its Neutral ID

    :type project_id: str
    :param project_id: neutral ID of a Project resource
    """
    try:
        project = Project.query.filter_by(neutral_id=project_id).one()
        payload = ProjectSchema(resource_linkage='categorisations').dump(project)
        return jsonify(payload)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()


@projects.route('/projects/<project_id>/categorisations')
@auth()
def projects_categorisations(project_id: str):
    """
    Returns Categorisation resources associated with a specific Project resource, specified by its Neutral ID

    :type project_id: str
    :param project_id: neutral ID of a Project resource
    """
    try:
        project = Project.query.filter_by(neutral_id=project_id).one()
        payload = ProjectSchema(related_resource='categorisations', many_related=True).dump(project)
        return jsonify(payload)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()
