# noinspection PyPackageRequirements
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
# noinspection PyPackageRequirements
from werkzeug.exceptions import NotFound, UnprocessableEntity
from flask import Blueprint, jsonify, request, current_app as app

from arctic_office_projects_api import auth
from arctic_office_projects_api.schemas import ProjectSchema, PersonSchema, ParticipantSchema
from arctic_office_projects_api.models import Project, Participant, Person

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
    )).dump(projects)

    return jsonify(payload.data)


@main.route('/projects/<project_id>')
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
        )).dump(project)
        return jsonify(payload.data)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()


@main.route('/projects/<project_id>/relationships/participants')
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
        return jsonify(payload.data)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()


@main.route('/projects/<project_id>/participants')
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
        return jsonify(payload.data)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()


@main.route('/participants')
@auth()
def participants_list():
    """
    Returns all Participant resources (People, Project association)

    The response is paginated.
    """
    page = request.args.get('page', type=int)
    if page is None:
        page = 1

    participants = Participant.query.paginate(page=page, per_page=app.config['APP_PAGE_SIZE'])
    payload = ParticipantSchema(many=True, paginate=True, include_data=(
        'project',
        'person'
    )).dump(participants)

    return jsonify(payload.data)


@main.route('/participants/<participant_id>')
@auth()
def participants_detail(participant_id: str):
    """
    Returns a specific Participant resource, specified by its Neutral ID

    :type participant_id: str
    :param participant_id: neutral ID of a Participant resource
    """
    try:
        participant = Participant.query.filter_by(neutral_id=participant_id).one()
        payload = ParticipantSchema(include_data=(
            'project',
            'person'
        )).dump(participant)
        return jsonify(payload.data)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()


@main.route('/participants/<participant_id>/relationships/projects')
@auth()
def participants_relationship_projects(participant_id: str):
    """
    Returns Project resource linkages associated with a specific Participant resource, specified by its Neutral ID

    :type participant_id: str
    :param participant_id: neutral ID of a Participant resource
    """
    try:
        participant = Participant.query.filter_by(neutral_id=participant_id).one()
        payload = ParticipantSchema(resource_linkage='project').dump(participant)
        return jsonify(payload.data)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()


@main.route('/participants/<participant_id>/relationships/people')
@auth()
def participants_relationship_people(participant_id: str):
    """
    Returns People resource linkages associated with a specific Participant resource, specified by its Neutral ID

    :type participant_id: str
    :param participant_id: neutral ID of a Participant resource
    """
    try:
        participant = Participant.query.filter_by(neutral_id=participant_id).one()
        payload = ParticipantSchema(resource_linkage='person').dump(participant)
        return jsonify(payload.data)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()


@main.route('/participants/<participant_id>/projects')
@auth()
def participants_projects(participant_id: str):
    """
    Returns the Project resource associated with a specific Participant resource, specified by its Neutral ID

    :type participant_id: str
    :param participant_id: neutral ID of a Participant resource
    """
    try:
        participant = Participant.query.filter_by(neutral_id=participant_id).one()
        payload = ParticipantSchema(related_resource='project', many_related=False).dump(participant)
        return jsonify(payload.data)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()


@main.route('/participants/<participant_id>/people')
@auth()
def participants_people(participant_id: str):
    """
    Returns the People resource associated with a specific Participant resource, specified by its Neutral ID

    :type participant_id: str
    :param participant_id: neutral ID of a Participant resource
    """
    try:
        participant = Participant.query.filter_by(neutral_id=participant_id).one()
        payload = ParticipantSchema(related_resource='person', many_related=False).dump(participant)
        return jsonify(payload.data)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()


@main.route('/people')
@auth()
def people_list():
    """
    Returns all People resources

    The response is paginated.
    """
    page = request.args.get('page', type=int)
    if page is None:
        page = 1

    people = Person.query.paginate(page=page, per_page=app.config['APP_PAGE_SIZE'])
    payload = PersonSchema(many=True, paginate=True, include_data=(
        'organisation',
        'participation',
        'participation.project'
    )).dump(people)

    return jsonify(payload.data)


@main.route('/people/<person_id>')
@auth()
def people_detail(person_id: str):
    """
    Returns a specific Person resource, specified by its Neutral ID

    :type person_id: str
    :param person_id: neutral ID of a Person resource
    """
    try:
        person = Person.query.filter_by(neutral_id=person_id).one()
        payload = PersonSchema(include_data=(
            'participation',
            'participation.project'
        )).dump(person)
        return jsonify(payload.data)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()


@main.route('/people/<person_id>/relationships/participants')
@auth()
def people_relationship_participants(person_id: str):
    """
    Returns Participant resource linkages associated with a specific Person resource, specified by its Neutral ID

    :type person_id: str
    :param person_id: neutral ID of a Person resource
    """
    try:
        person = Person.query.filter_by(neutral_id=person_id).one()
        payload = PersonSchema(resource_linkage='participation').dump(person)
        return jsonify(payload.data)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()


@main.route('/people/<person_id>/participants')
@auth()
def people_participants(person_id: str):
    """
    Returns Participant resources associated with a specific Person resource, specified by its Neutral ID

    :type person_id: str
    :param person_id: neutral ID of a Person resource
    """
    try:
        person = Person.query.filter_by(neutral_id=person_id).one()
        payload = PersonSchema(related_resource='participation', many_related=True).dump(person)
        return jsonify(payload.data)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()
