# noinspection PyPackageRequirements
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
# noinspection PyPackageRequirements
from werkzeug.exceptions import NotFound, UnprocessableEntity
from flask import Blueprint, jsonify, request, current_app as app

from arctic_office_projects_api import auth
from arctic_office_projects_api.schemas import CategorySchemeSchema
from arctic_office_projects_api.models import CategoryScheme

category_schemes = Blueprint('category_schemes', __name__)


@category_schemes.route('/category-schemes')
@auth()
def category_schemes_list():
    """
    Returns all CategoryScheme resources

    The response is paginated.
    """
    page = request.args.get('page', type=int)
    if page is None:
        page = 1

    _category_schemes = CategoryScheme.query.paginate(page=page, per_page=app.config['APP_PAGE_SIZE'])
    payload = CategorySchemeSchema(many=True, paginate=True, include_data=(
        'categories',
        'categories.categorisations.project'
    )).dump(_category_schemes)

    return jsonify(payload.data)


@category_schemes.route('/category-schemes/<category_scheme_id>')
@auth()
def category_schemes_detail(category_scheme_id: str):
    """
    Returns a specific CategoryScheme resource, specified by its Neutral ID

    :type category_scheme_id: str
    :param category_scheme_id: neutral ID of a CategoryTerm resource
    """
    try:
        category_scheme = CategoryScheme.query.filter_by(neutral_id=category_scheme_id).one()
        payload = CategorySchemeSchema(include_data=(
            'categories',
            'categories.categorisations.project'
        )).dump(category_scheme)
        return jsonify(payload.data)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()


@category_schemes.route('/category-schemes/<category_scheme_id>/relationships/categories')
@auth()
def category_schemes_relationship_category_terms(category_scheme_id: str):
    """
    Returns CategoryTerm resource linkages associated with a specific CategoryScheme resource, specified by its Neutral
    ID

    :type category_scheme_id: str
    :param category_scheme_id: neutral ID of a CategoryTerm resource
    """
    try:
        category_scheme = CategoryScheme.query.filter_by(neutral_id=category_scheme_id).one()
        payload = CategorySchemeSchema(resource_linkage='categories').dump(category_scheme)
        return jsonify(payload.data)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()


@category_schemes.route('/category-schemes/<category_scheme_id>/categories')
@auth()
def category_schemes_category_terms(category_scheme_id: str):
    """
    Returns CategoryTerm resources associated with a specific CategoryScheme resource, specified by its Neutral ID

    :type category_scheme_id: str
    :param category_scheme_id: neutral ID of a CategoryTerm resource
    """
    try:
        category_scheme = CategoryScheme.query.filter_by(neutral_id=category_scheme_id).one()
        payload = CategorySchemeSchema(related_resource='categories', many_related=True).dump(category_scheme)
        return jsonify(payload.data)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()
