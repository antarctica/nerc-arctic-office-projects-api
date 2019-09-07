# noinspection PyPackageRequirements
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
# noinspection PyPackageRequirements
from werkzeug.exceptions import NotFound, UnprocessableEntity
from flask import Blueprint, jsonify, request, current_app as app

from arctic_office_projects_api import auth
from arctic_office_projects_api.schemas import CategorisationSchema
from arctic_office_projects_api.models import Categorisation

categorisations = Blueprint('categorisations', __name__)


@categorisations.route('/categorisations')
@auth()
def categorisations_list():
    """
    Returns all Categorisation resources

    The response is paginated.
    """
    page = request.args.get('page', type=int)
    if page is None:
        page = 1

    _categorisations = Categorisation.query.paginate(page=page, per_page=app.config['APP_PAGE_SIZE'])
    payload = CategorisationSchema(many=True, paginate=True, include_data=(
        'project',
        'category',
        'category.parent_category',
        'category.category_scheme'
    )).dump(_categorisations)

    return jsonify(payload)


@categorisations.route('/categorisations/<categorisation_id>')
@auth()
def categorisations_detail(categorisation_id: str):
    """
    Returns a specific Categorisation resource, specified by its Neutral ID

    :type categorisation_id: str
    :param categorisation_id: neutral ID of a Categorisation resource
    """
    try:
        categorisation = Categorisation.query.filter_by(neutral_id=categorisation_id).one()
        payload = CategorisationSchema(include_data=(
            'project',
            'category',
            'category.parent_category',
            'category.category_scheme'
        )).dump(categorisation)
        return jsonify(payload)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()


@categorisations.route('/categorisations/<categorisation_id>/relationships/projects')
@auth()
def categorisations_relationship_projects(categorisation_id: str):
    """
    Returns Project resource linkages associated with a specific Categorisation resource, specified by its Neutral ID

    :type categorisation_id: str
    :param categorisation_id: neutral ID of a CategoryTerm resource
    """
    try:
        categorisation = Categorisation.query.filter_by(neutral_id=categorisation_id).one()
        payload = CategorisationSchema(resource_linkage='project').dump(categorisation)
        return jsonify(payload)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()


@categorisations.route('/categorisations/<categorisation_id>/relationships/categories')
@auth()
def categorisations_relationship_category_terms(categorisation_id: str):
    """
    Returns CategoryTerm resource linkages associated with a specific Categorisation resource, specified by its Neutral
    ID

    :type categorisation_id: str
    :param categorisation_id: neutral ID of a CategoryTerm resource
    """
    try:
        categorisation = Categorisation.query.filter_by(neutral_id=categorisation_id).one()
        payload = CategorisationSchema(resource_linkage='category').dump(categorisation)
        return jsonify(payload)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()


@categorisations.route('/categorisations/<categorisation_id>/projects')
@auth()
def categorisations_projects(categorisation_id: str):
    """
    Returns Project resources associated with a specific Categorisation resource, specified by its Neutral ID

    :type categorisation_id: str
    :param categorisation_id: neutral ID of a CategoryTerm resource
    """
    try:
        categorisation = Categorisation.query.filter_by(neutral_id=categorisation_id).one()
        payload = CategorisationSchema(related_resource='project', many_related=False).dump(categorisation)
        return jsonify(payload)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()


@categorisations.route('/categorisations/<categorisation_id>/categories')
@auth()
def categorisations_category_terms(categorisation_id: str):
    """
    Returns CategoryTerm resources associated with a specific Categorisation resource, specified by its Neutral ID

    :type categorisation_id: str
    :param categorisation_id: neutral ID of a CategoryTerm resource
    """
    try:
        categorisation = Categorisation.query.filter_by(neutral_id=categorisation_id).one()
        payload = CategorisationSchema(related_resource='category', many_related=False).dump(categorisation)
        return jsonify(payload)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()
