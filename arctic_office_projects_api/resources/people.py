# noinspection PyPackageRequirements
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
# noinspection PyPackageRequirements
from werkzeug.exceptions import NotFound, UnprocessableEntity
from flask import Blueprint, jsonify, request, current_app as app

from arctic_office_projects_api import auth
from arctic_office_projects_api.schemas import PersonSchema
from arctic_office_projects_api.models import Person

people = Blueprint('people', __name__)


@people.route('/people')
@auth()
def people_list():
    """
    Returns all People resources

    The response is paginated.
    """
    page = request.args.get('page', type=int)
    if page is None:
        page = 1

    _people = Person.query.paginate(page=page, per_page=app.config['APP_PAGE_SIZE'])
    payload = PersonSchema(many=True, paginate=True, include_data=(
        'organisation',
        'participation',
        'participation.project'
    )).dump(_people)

    return jsonify(payload.data)


@people.route('/people/<person_id>')
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


@people.route('/people/<person_id>/relationships/participants')
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


@people.route('/people/<person_id>/relationships/organisations')
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


@people.route('/people/<person_id>/participants')
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


@people.route('/people/<person_id>/organisations')
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
