# noinspection PyPackageRequirements
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
# noinspection PyPackageRequirements
from werkzeug.exceptions import NotFound, UnprocessableEntity
from flask import Blueprint, jsonify, request, current_app as app

from arctic_office_projects_api import auth
from arctic_office_projects_api.schemas import OrganisationSchema
from arctic_office_projects_api.models import Organisation

organisations = Blueprint('organisations', __name__)


@organisations.route('/organisations')
@auth()
def organisations_list():
    """
    Returns all Organisation resources

    The response is paginated.
    """
    page = request.args.get('page', type=int)
    if page is None:
        page = 1

    _organisations = Organisation.query.paginate(page=page, per_page=app.config['APP_PAGE_SIZE'])
    payload = OrganisationSchema(many=True, paginate=True, include_data=(
        'people',
        'people.participation',
        'people.participation.project',
        'grants',
        'grants.allocations',
        'grants.allocations.project'
    )).dump(_organisations)

    return jsonify(payload.data)


@organisations.route('/organisations/<organisation_id>')
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


@organisations.route('/organisations/<organisation_id>/relationships/people')
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


@organisations.route('/organisations/<organisation_id>/relationships/grants')
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


@organisations.route('/organisations/<organisation_id>/people')
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


@organisations.route('/organisations/<organisation_id>/grants')
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
