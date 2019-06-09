# noinspection PyPackageRequirements
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
# noinspection PyPackageRequirements
from werkzeug.exceptions import NotFound, UnprocessableEntity
from flask import Blueprint, jsonify, request, current_app as app

from arctic_office_projects_api import auth
from arctic_office_projects_api.schemas import GrantSchema
from arctic_office_projects_api.models import Grant

grants = Blueprint('grants', __name__)


@grants.route('/grants')
@auth()
def grants_list():
    """
    Returns all Grant resources

    The response is paginated.
    """
    page = request.args.get('page', type=int)
    if page is None:
        page = 1

    _grants = Grant.query.paginate(page=page, per_page=app.config['APP_PAGE_SIZE'])
    payload = GrantSchema(many=True, paginate=True, include_data=(
        'funder',
        'allocations',
        'allocations.project'
    )).dump(_grants)

    return jsonify(payload.data)


@grants.route('/grants/<grant_id>')
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


@grants.route('/grants/<grant_id>/relationships/allocations')
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


@grants.route('/grants/<grant_id>/relationships/organisations')
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


@grants.route('/grants/<grant_id>/allocations')
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


@grants.route('/grants/<grant_id>/organisations')
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
