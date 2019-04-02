# noinspection PyPackageRequirements
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
# noinspection PyPackageRequirements
from werkzeug.exceptions import NotFound, UnprocessableEntity
from flask import Blueprint, jsonify, request, current_app as app

from arctic_office_projects_api import auth
from arctic_office_projects_api.schemas import ProjectSchema, PersonSchema, ParticipantSchema, GrantSchema, \
    AllocationSchema, OrganisationSchema
from arctic_office_projects_api.models import Project, Participant, Person, Grant, Allocation, Organisation

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
        'participants.person.organisation',
        'allocations',
        'allocations.grant',
        'allocations.grant.funder'
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
            'participants.person.organisation',
            'allocations',
            'allocations.grant',
            'allocations.grant.funder'
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


@main.route('/projects/<project_id>/relationships/allocations')
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


@main.route('/projects/<project_id>/allocations')
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
            'organisation',
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


@main.route('/people/<person_id>/relationships/organisations')
@auth()
def people_relationship_organisations(person_id: str):
    """
    Returns Organisation resource linkages associated with a specific Person resource, specified by its Neutral ID

    :type person_id: str
    :param person_id: neutral ID of a Person resource
    """
    try:
        person = Person.query.filter_by(neutral_id=person_id).one()
        payload = PersonSchema(resource_linkage='organisation').dump(person)
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


@main.route('/people/<person_id>/organisations')
@auth()
def people_organisations(person_id: str):
    """
    Returns Organisation resources associated with a specific Person resource, specified by its Neutral ID

    :type person_id: str
    :param person_id: neutral ID of a Person resource
    """
    try:
        person = Person.query.filter_by(neutral_id=person_id).one()
        payload = PersonSchema(related_resource='organisation', many_related=False).dump(person)
        return jsonify(payload.data)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()


@main.route('/grants')
@auth()
def grants_list():
    """
    Returns all Grant resources

    The response is paginated.
    """
    page = request.args.get('page', type=int)
    if page is None:
        page = 1

    grants = Grant.query.paginate(page=page, per_page=app.config['APP_PAGE_SIZE'])
    payload = GrantSchema(many=True, paginate=True, include_data=(
        'funder',
        'allocations',
        'allocations.project'
    )).dump(grants)

    return jsonify(payload.data)


@main.route('/grants/<grant_id>')
@auth()
def grants_detail(grant_id: str):
    """
    Returns a specific Grant resource, specified by its Neutral ID

    :type grant_id: str
    :param grant_id: neutral ID of a Grant resource
    """
    try:
        grant = Grant.query.filter_by(neutral_id=grant_id).one()
        payload = GrantSchema(include_data=(
            'funder',
            'allocations',
            'allocations.project'
        )).dump(grant)
        return jsonify(payload.data)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()


@main.route('/grants/<grant_id>/relationships/allocations')
@auth()
def grants_relationship_allocations(grant_id: str):
    """
    Returns Allocation resource linkages associated with a specific Grant resource, specified by its Neutral ID

    :type grant_id: str
    :param grant_id: neutral ID of a Grant resource
    """
    try:
        grant = Grant.query.filter_by(neutral_id=grant_id).one()
        payload = GrantSchema(resource_linkage='allocations').dump(grant)
        return jsonify(payload.data)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()


@main.route('/grants/<grant_id>/relationships/organisations')
@auth()
def grants_relationship_organisations(grant_id: str):
    """
    Returns Organisation resource linkages associated with a specific Grant resource, specified by its Neutral ID

    :type grant_id: str
    :param grant_id: neutral ID of a Grant resource
    """
    try:
        grant = Grant.query.filter_by(neutral_id=grant_id).one()
        payload = GrantSchema(resource_linkage='funder').dump(grant)
        return jsonify(payload.data)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()


@main.route('/grants/<grant_id>/allocations')
@auth()
def grants_allocations(grant_id: str):
    """
    Returns Allocation resources associated with a specific Grant resource, specified by its Neutral ID

    :type grant_id: str
    :param grant_id: neutral ID of a Grant resource
    """
    try:
        grant = Grant.query.filter_by(neutral_id=grant_id).one()
        payload = GrantSchema(related_resource='allocations', many_related=True).dump(grant)
        return jsonify(payload.data)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()


@main.route('/grants/<grant_id>/organisations')
@auth()
def grants_organisations(grant_id: str):
    """
    Returns Organisation resources associated with a specific Grant resource, specified by its Neutral ID

    :type grant_id: str
    :param grant_id: neutral ID of a Grant resource
    """
    try:
        grant = Grant.query.filter_by(neutral_id=grant_id).one()
        payload = GrantSchema(related_resource='funder', many_related=False).dump(grant)
        return jsonify(payload.data)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()


@main.route('/allocations')
@auth()
def allocations_list():
    """
    Returns all Allocation resources (Grant, Project association)

    The response is paginated.
    """
    page = request.args.get('page', type=int)
    if page is None:
        page = 1

    allocations = Allocation.query.paginate(page=page, per_page=app.config['APP_PAGE_SIZE'])
    payload = AllocationSchema(many=True, paginate=True, include_data=(
        'project',
        'grant'
    )).dump(allocations)

    return jsonify(payload.data)


@main.route('/allocations/<allocation_id>')
@auth()
def allocations_detail(allocation_id: str):
    """
    Returns a specific Allocation resource, specified by its Neutral ID

    :type allocation_id: str
    :param allocation_id: neutral ID of a Allocation resource
    """
    try:
        allocation = Allocation.query.filter_by(neutral_id=allocation_id).one()
        payload = AllocationSchema(include_data=(
            'project',
            'grant'
        )).dump(allocation)
        return jsonify(payload.data)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()


@main.route('/allocations/<allocation_id>/relationships/projects')
@auth()
def allocations_relationship_projects(allocation_id: str):
    """
    Returns Project resource linkages associated with a specific Allocation resource, specified by its Neutral ID

    :type allocation_id: str
    :param allocation_id: neutral ID of a Allocation resource
    """
    try:
        allocation = Allocation.query.filter_by(neutral_id=allocation_id).one()
        payload = AllocationSchema(resource_linkage='project').dump(allocation)
        return jsonify(payload.data)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()


@main.route('/allocations/<allocation_id>/relationships/grants')
@auth()
def allocations_relationship_grants(allocation_id: str):
    """
    Returns Grant resource linkages associated with a specific Allocation resource, specified by its Neutral ID

    :type allocation_id: str
    :param allocation_id: neutral ID of a Allocation resource
    """
    try:
        allocation = Allocation.query.filter_by(neutral_id=allocation_id).one()
        payload = AllocationSchema(resource_linkage='grant').dump(allocation)
        return jsonify(payload.data)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()


@main.route('/allocations/<allocation_id>/projects')
@auth()
def allocations_projects(allocation_id: str):
    """
    Returns the Project resource associated with a specific Allocation resource, specified by its Neutral ID

    :type allocation_id: str
    :param allocation_id: neutral ID of a Allocation resource
    """
    try:
        allocation = Allocation.query.filter_by(neutral_id=allocation_id).one()
        payload = AllocationSchema(related_resource='project', many_related=False).dump(allocation)
        return jsonify(payload.data)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()


@main.route('/allocations/<allocation_id>/grants')
@auth()
def allocations_grants(allocation_id: str):
    """
    Returns the People resource associated with a specific Allocation resource, specified by its Neutral ID

    :type allocation_id: str
    :param allocation_id: neutral ID of a Allocation resource
    """
    try:
        allocation = Allocation.query.filter_by(neutral_id=allocation_id).one()
        payload = AllocationSchema(related_resource='grant', many_related=False).dump(allocation)
        return jsonify(payload.data)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()


@main.route('/organisations')
@auth()
def organisations_list():
    """
    Returns all Organisation resources

    The response is paginated.
    """
    page = request.args.get('page', type=int)
    if page is None:
        page = 1

    organisations = Organisation.query.paginate(page=page, per_page=app.config['APP_PAGE_SIZE'])
    payload = OrganisationSchema(many=True, paginate=True, include_data=(
        'people',
        'people.participation',
        'people.participation.project',
        'grants',
        'grants.allocations',
        'grants.allocations.project'
    )).dump(organisations)

    return jsonify(payload.data)


@main.route('/organisations/<organisation_id>')
@auth()
def organisations_detail(organisation_id: str):
    """
    Returns a specific Organisation resource, specified by its Neutral ID

    :type organisation_id: str
    :param organisation_id: neutral ID of a Organisation resource
    """
    try:
        organisation = Organisation.query.filter_by(neutral_id=organisation_id).one()
        payload = OrganisationSchema(include_data=(
            'people',
            'people.participation',
            'people.participation.project',
            'grants',
            'grants.allocations',
            'grants.allocations.project'
        )).dump(organisation)
        return jsonify(payload.data)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()


@main.route('/organisations/<organisation_id>/relationships/people')
@auth()
def organisations_relationship_people(organisation_id: str):
    """
    Returns Person resource linkages associated with a specific Organisation resource, specified by its Neutral ID

    :type organisation_id: str
    :param organisation_id: neutral ID of a Organisation resource
    """
    try:
        organisation = Organisation.query.filter_by(neutral_id=organisation_id).one()
        payload = OrganisationSchema(resource_linkage='people').dump(organisation)
        return jsonify(payload.data)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()


@main.route('/organisations/<organisation_id>/relationships/grants')
@auth()
def organisations_relationship_grants(organisation_id: str):
    """
    Returns Grant resource linkages associated with a specific Organisation resource, specified by its Neutral ID

    :type organisation_id: str
    :param organisation_id: neutral ID of a Organisation resource
    """
    try:
        organisation = Organisation.query.filter_by(neutral_id=organisation_id).one()
        payload = OrganisationSchema(resource_linkage='grants').dump(organisation)
        return jsonify(payload.data)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()


@main.route('/organisations/<organisation_id>/people')
@auth()
def organisations_people(organisation_id: str):
    """
    Returns Person resources associated with a specific Organisation resource, specified by its Neutral ID

    :type organisation_id: str
    :param organisation_id: neutral ID of a Organisation resource
    """
    try:
        organisation = Organisation.query.filter_by(neutral_id=organisation_id).one()
        payload = OrganisationSchema(related_resource='people', many_related=True).dump(organisation)
        return jsonify(payload.data)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()


@main.route('/organisations/<organisation_id>/grants')
@auth()
def organisations_grants(organisation_id: str):
    """
    Returns Grant resources associated with a specific Organisation resource, specified by its Neutral ID

    :type organisation_id: str
    :param organisation_id: neutral ID of a Organisation resource
    """
    try:
        organisation = Organisation.query.filter_by(neutral_id=organisation_id).one()
        payload = OrganisationSchema(related_resource='grants', many_related=True).dump(organisation)
        return jsonify(payload.data)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()
