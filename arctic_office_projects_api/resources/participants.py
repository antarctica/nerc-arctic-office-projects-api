# noinspection PyPackageRequirements
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
# noinspection PyPackageRequirements
from werkzeug.exceptions import NotFound, UnprocessableEntity
from flask import Blueprint, jsonify, request, current_app as app

from arctic_office_projects_api import auth
from arctic_office_projects_api.schemas import ParticipantSchema
from arctic_office_projects_api.models import Participant

participants = Blueprint('participants', __name__)


@participants.route('/participants')
@auth()
def participants_list():
    """
    Returns all Participant resources (People, Project association)

    The response is paginated.
    """
    page = request.args.get('page', type=int)
    if page is None:
        page = 1

    _participants = Participant.query.paginate(page=page, per_page=app.config['APP_PAGE_SIZE'])
    payload = ParticipantSchema(many=True, paginate=True, include_data=(
        'project',
        'person'
    )).dump(_participants)

    return jsonify(payload)


@participants.route('/participants/<participant_id>')
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
        return jsonify(payload)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()


@participants.route('/participants/<participant_id>/relationships/projects')
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
        return jsonify(payload)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()


@participants.route('/participants/<participant_id>/relationships/people')
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
        return jsonify(payload)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()


@participants.route('/participants/<participant_id>/projects')
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
        return jsonify(payload)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()


@participants.route('/participants/<participant_id>/people')
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
        return jsonify(payload)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()
