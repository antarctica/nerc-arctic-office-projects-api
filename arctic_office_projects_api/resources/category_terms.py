import os

# noinspection PyPackageRequirements
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

# noinspection PyPackageRequirements
from werkzeug.exceptions import NotFound, UnprocessableEntity
from flask import Blueprint, jsonify, request, current_app as app

from arctic_office_projects_api.utils import conditional_decorator
from arctic_office_projects_api import auth
from arctic_office_projects_api.schemas import CategoryTermSchema
from arctic_office_projects_api.models import CategoryTerm

category_terms = Blueprint("category_terms", __name__)

flask_env = os.getenv("FLASK_ENV")
is_production = False
if flask_env == "production" or flask_env == "staging":
    is_production = True


@category_terms.route("/categories")
@conditional_decorator(auth(), is_production)
def category_terms_list():
    """
    Returns all CategoryTerm resources

    The response is paginated.
    """
    page = request.args.get("page", type=int)
    if page is None:
        page = 1

    _category_terms = CategoryTerm.query.paginate(
        page=page, per_page=app.config["APP_PAGE_SIZE"]
    )
    payload = CategoryTermSchema(
        many=True,
        paginate=True,
        include_data=(
            "parent_category",
            "categorisations",
            "categorisations.project",
            "category_scheme",
        ),
    ).dump(_category_terms)

    return jsonify(payload)


@category_terms.route("/categories/<category_term_id>")
@conditional_decorator(auth(), is_production)
def category_terms_detail(category_term_id: str):
    """
    Returns a specific CategoryTerm resource, specified by its Neutral ID

    :type category_term_id: str
    :param category_term_id: neutral ID of a CategoryTerm resource
    """
    try:
        category_term = CategoryTerm.query.filter_by(neutral_id=category_term_id).one()
        payload = CategoryTermSchema(
            include_data=(
                "parent_category",
                "categorisations",
                "categorisations.project",
                "category_scheme",
            )
        ).dump(category_term)
        return jsonify(payload)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()


@category_terms.route("/categories/<category_term_id>/relationships/parent-categories")
@conditional_decorator(auth(), is_production)
def category_terms_relationship_parent_category_terms(category_term_id: str):
    """
    Returns parent CategoryTerm resource linkages for a specific CategoryTerm resource, specified by its Neutral ID

    :type category_term_id: str
    :param category_term_id: neutral ID of a CategoryTerm resource
    """
    try:
        category_term = CategoryTerm.query.filter_by(neutral_id=category_term_id).one()
        payload = CategoryTermSchema(resource_linkage="parent-category").dump(
            category_term
        )
        return jsonify(payload)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()


@category_terms.route("/categories/<category_term_id>/relationships/category-schemes")
@conditional_decorator(auth(), is_production)
def category_terms_relationship_category_schemes(category_term_id: str):
    """
    Returns CategoryScheme resource linkages associated with a specific CategoryTerm resource, specified by its Neutral
    ID

    :type category_term_id: str
    :param category_term_id: neutral ID of a CategoryTerm resource
    """
    try:
        category_term = CategoryTerm.query.filter_by(neutral_id=category_term_id).one()
        payload = CategoryTermSchema(resource_linkage="category-scheme").dump(
            category_term
        )
        return jsonify(payload)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()


@category_terms.route("/categories/<category_term_id>/relationships/categorisations")
@conditional_decorator(auth(), is_production)
def category_terms_relationship_categorisations(category_term_id: str):
    """
    Returns Categorisation resource linkages associated with a specific CategoryTerm resource, specified by its Neutral
    ID

    :type category_term_id: str
    :param category_term_id: neutral ID of a CategoryTerm resource
    """
    try:
        category_term = CategoryTerm.query.filter_by(neutral_id=category_term_id).one()
        payload = CategoryTermSchema(resource_linkage="categorisations").dump(
            category_term
        )
        return jsonify(payload)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()


@category_terms.route("/categories/<category_term_id>/parent-categories")
@conditional_decorator(auth(), is_production)
def category_terms_parent_category_terms(category_term_id: str):
    """
    Returns parent CategoryTerm resources associated with a specific CategoryTerm resource, specified by its Neutral ID

    :type category_term_id: str
    :param category_term_id: neutral ID of a CategoryTerm resource
    """
    try:
        category_term = CategoryTerm.query.filter_by(neutral_id=category_term_id).one()
        payload = CategoryTermSchema(
            related_resource="parent_category", many_related=False
        ).dump(category_term)
        return jsonify(payload)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()


@category_terms.route("/categories/<category_term_id>/category-schemes")
@conditional_decorator(auth(), is_production)
def category_terms_category_schemes(category_term_id: str):
    """
    Returns CategoryScheme resources associated with a specific CategoryTerm resource, specified by its Neutral ID

    :type category_term_id: str
    :param category_term_id: neutral ID of a CategoryTerm resource
    """
    try:
        category_term = CategoryTerm.query.filter_by(neutral_id=category_term_id).one()
        payload = CategoryTermSchema(
            related_resource="category_scheme", many_related=False
        ).dump(category_term)
        return jsonify(payload)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()


@category_terms.route("/categories/<category_term_id>/categorisations")
@conditional_decorator(auth(), is_production)
def category_terms_categorisations(category_term_id: str):
    """
    Returns Categorisation resources associated with a specific CategoryTerm resource, specified by its Neutral ID

    :type category_term_id: str
    :param category_term_id: neutral ID of a CategoryTerm resource
    """
    try:
        category_term = CategoryTerm.query.filter_by(neutral_id=category_term_id).one()
        payload = CategoryTermSchema(
            related_resource="categorisations", many_related=True
        ).dump(category_term)
        return jsonify(payload)
    except NoResultFound:
        raise NotFound()
    except MultipleResultsFound:
        raise UnprocessableEntity()
