# noinspection PyPackageRequirements
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
# noinspection PyPackageRequirements
from werkzeug.exceptions import NotFound, UnprocessableEntity
from flask import Blueprint, jsonify, request, current_app as app

from arctic_office_projects_api import auth
from arctic_office_projects_api.schemas import AllocationSchema
from arctic_office_projects_api.models import Allocation

allocations = Blueprint('allocations', __name__)


@allocations.route('/allocations')
@auth()
def allocations_list():
    """
    Returns all Allocation resources (Grant, Project association)

    The response is paginated.
    """
    page = request.args.get('page', type=int)
    if page is None:
        page = 1

    _allocations = Allocation.query.paginate(page=page, per_page=app.config['APP_PAGE_SIZE'])
    payload = AllocationSchema(many=True, paginate=True, include_data=(
        'project',
        'grant'
    )).dump(_allocations)

    return jsonify(payload.data)


@allocations.route('/allocations/<allocation_id>')
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


@allocations.route('/allocations/<allocation_id>/relationships/projects')
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


@allocations.route('/allocations/<allocation_id>/relationships/grants')
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


@allocations.route('/allocations/<allocation_id>/projects')
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


@allocations.route('/allocations/<allocation_id>/grants')
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
