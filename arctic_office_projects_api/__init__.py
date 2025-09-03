import os
import logging
# import sentry_sdk
from functools import wraps
from flask import Flask, jsonify, request
from flask.logging import default_handler

import jwt
from jwt import PyJWKClient

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

# noinspection PyPackageRequirements
from werkzeug.exceptions import (
    BadRequest,
    NotFound,
    InternalServerError,
    UnprocessableEntity,
)

# from config import config
from arctic_office_projects_api.utils import RequestFormatter
from arctic_office_projects_api.extensions import db
from arctic_office_projects_api.errors import (
    error_handler_generic_bad_request,
    error_handler_generic_not_found,
    error_handler_generic_internal_server_error,
    error_handler_generic_unprocessable_entity,
)
from arctic_office_projects_api.commands import (
    seeding_cli_group,
    importing_cli_group,
)
from arctic_office_projects_api.routes import index_route, healthcheck_route

from arctic_office_projects_api.schemas import ProjectSchema
from arctic_office_projects_api.models import Project
from arctic_office_projects_api.schemas import PersonSchema
from arctic_office_projects_api.models import Person
from arctic_office_projects_api.schemas import GrantSchema
from arctic_office_projects_api.models import Grant
from arctic_office_projects_api.schemas import OrganisationSchema
from arctic_office_projects_api.models import Organisation
from arctic_office_projects_api.schemas import CategorySchemeSchema
from arctic_office_projects_api.models import CategoryScheme
from arctic_office_projects_api.schemas import CategoryTermSchema
from arctic_office_projects_api.models import CategoryTerm
from arctic_office_projects_api.schemas import ParticipantSchema
from arctic_office_projects_api.models import Participant
from arctic_office_projects_api.schemas import AllocationSchema
from arctic_office_projects_api.models import Allocation
from arctic_office_projects_api.schemas import CategorisationSchema
from arctic_office_projects_api.models import Categorisation


def validate_token(token):
    TENANT_ID = os.getenv("ENTRA_AUTH_TENANT_ID")
    CLIENT_ID = os.getenv("ENTRA_AUTH_CLIENT_ID")

    if not TENANT_ID or not CLIENT_ID:
        raise Exception("Missing TENANT_ID or CLIENT_ID in environment variables")

    jwks_url = f"https://login.microsoftonline.com/{TENANT_ID}/discovery/v2.0/keys"
    jwk_client = PyJWKClient(jwks_url)
    signing_key = jwk_client.get_signing_key_from_jwt(token)

    decoded_token = jwt.decode(
        token,
        signing_key.key,
        algorithms=["RS256"],
        audience=CLIENT_ID,
        issuer=f"https://login.microsoftonline.com/{TENANT_ID}/v2.0",
    )
    return decoded_token


def auth_required():
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get("Authorization", None)
            if not auth_header or not auth_header.startswith("Bearer "):
                return jsonify({"error": "Missing or invalid Authorization header"}), 401

            token = auth_header.split(" ")[1]
            try:
                request.token_payload = validate_token(token)
            except Exception as e:
                return jsonify({"error": "Invalid token", "detail": str(e)}), 401

            return f(*args, **kwargs)
        return wrapper
    return decorator


def create_app(config_name):
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI") or None
    app.config["APP_PAGE_SIZE"] = int(os.getenv('APP_PAGE_SIZE') or 10)

    db.init_app(app)
    app.auth = auth_required

    # Logging
    formatter = RequestFormatter(
        "[%(asctime)s] [%(levelname)s] [%(request_id)s] [%(url)s]: %(message)s"
    )
    default_handler.setFormatter(formatter)
    level = os.getenv('LOGGING_LEVEL', 'INFO')
    default_handler.setLevel(getattr(logging, level, logging.INFO))

    # Error handlers
    app.register_error_handler(BadRequest, error_handler_generic_bad_request)
    app.register_error_handler(NotFound, error_handler_generic_not_found)
    app.register_error_handler(
        UnprocessableEntity, error_handler_generic_unprocessable_entity
    )
    app.register_error_handler(
        InternalServerError, error_handler_generic_internal_server_error
    )

    # CLI commands
    app.cli.add_command(seeding_cli_group)
    app.cli.add_command(importing_cli_group)

    # Routes
    app.add_url_rule("/", "index", index_route, methods=["get", "options"])

    app.add_url_rule(
        "/healthcheck",
        "healthcheck",
        healthcheck_route,
        methods=["get", "options"]
    )

    # is_testing = app.config.get("TESTING")

    # Resources
    @app.route("/projects")
    @app.auth()
    def projects_list():
        """
        Returns all Project resources

        The response is paginated.
        """
        page = request.args.get("page", type=int)
        if page is None:
            page = 1

        projects = Project.query.paginate(
            page=page, per_page=app.config["APP_PAGE_SIZE"]
        )
        payload = ProjectSchema(
            many=True,
            paginate=True,
            include_data=(
                "participants",
                "participants.person",
                "participants.person.organisation",
                "allocations",
                "allocations.grant",
                "allocations.grant.funder",
                "categorisations",
                "categorisations.category",
                "categorisations.category.category_scheme",
                "categorisations.category.parent_category",
            ),
        ).dump(projects)

        return jsonify(payload)

    @app.route("/projects/<project_id>")
    @app.auth()
    def projects_detail(project_id: str):
        """
        Returns a specific Project resource, specified by its Neutral ID

        :type project_id: str
        :param project_id: neutral ID of a Project resource
        """
        try:
            project = Project.query.filter_by(neutral_id=project_id).one()
            payload = ProjectSchema(
                include_data=(
                    "participants",
                    "participants.person",
                    "participants.person.organisation",
                    "allocations",
                    "allocations.grant",
                    "allocations.grant.funder",
                    "categorisations",
                    "categorisations.category",
                    "categorisations.category.category_scheme",
                    "categorisations.category.parent_category",
                )
            ).dump(project)
            return jsonify(payload)
        except NoResultFound:
            raise NotFound()
        except MultipleResultsFound:  # pragma: no cover
            raise UnprocessableEntity()  # pragma: no cover

    @app.route("/projects/<project_id>/relationships/participants")
    @app.auth()
    def projects_relationship_participants(project_id: str):
        """
        Returns Participant resource linkages associated with a specific Project resource, specified by its Neutral ID

        :type project_id: str
        :param project_id: neutral ID of a Project resource
        """
        try:
            project = Project.query.filter_by(neutral_id=project_id).one()
            payload = ProjectSchema(resource_linkage="participants").dump(project)
            return jsonify(payload)
        except NoResultFound:
            raise NotFound()
        except MultipleResultsFound:  # pragma: no cover
            raise UnprocessableEntity()  # pragma: no cover

    @app.route("/projects/<project_id>/relationships/allocations")
    @app.auth()
    def projects_relationship_allocations(project_id: str):
        """
        Returns Allocation resource linkages associated with a specific Project resource, specified by its Neutral ID

        :type project_id: str
        :param project_id: neutral ID of a Project resource
        """
        try:
            project = Project.query.filter_by(neutral_id=project_id).one()
            payload = ProjectSchema(resource_linkage="allocations").dump(project)
            return jsonify(payload)
        except NoResultFound:
            raise NotFound()
        except MultipleResultsFound:  # pragma: no cover
            raise UnprocessableEntity()  # pragma: no cover

    @app.route("/projects/<project_id>/participants")
    @app.auth()
    def projects_participants(project_id: str):
        """
        Returns Participant resources associated with a specific Project resource, specified by its Neutral ID

        :type project_id: str
        :param project_id: neutral ID of a Project resource
        """
        try:
            project = Project.query.filter_by(neutral_id=project_id).one()
            payload = ProjectSchema(
                related_resource="participants", many_related=True
            ).dump(project)
            return jsonify(payload)
        except NoResultFound:
            raise NotFound()
        except MultipleResultsFound:  # pragma: no cover
            raise UnprocessableEntity()  # pragma: no cover

    @app.route("/projects/<project_id>/allocations")
    @app.auth()
    def projects_allocations(project_id: str):
        """
        Returns Allocation resources associated with a specific Project resource, specified by its Neutral ID

        :type project_id: str
        :param project_id: neutral ID of a Project resource
        """
        try:
            project = Project.query.filter_by(neutral_id=project_id).one()
            payload = ProjectSchema(
                related_resource="allocations", many_related=True
            ).dump(project)
            return jsonify(payload)
        except NoResultFound:
            raise NotFound()
        except MultipleResultsFound:  # pragma: no cover
            raise UnprocessableEntity()  # pragma: no cover

    @app.route("/projects/<project_id>/relationships/categorisations")
    @app.auth()
    def projects_relationship_categorisations(project_id: str):
        """
        Returns Categorisation resource linkages associated with a specific Project resource, specified by its Neutral ID

        :type project_id: str
        :param project_id: neutral ID of a Project resource
        """
        try:
            project = Project.query.filter_by(neutral_id=project_id).one()
            payload = ProjectSchema(resource_linkage="categorisations").dump(project)
            return jsonify(payload)
        except NoResultFound:
            raise NotFound()
        except MultipleResultsFound:  # pragma: no cover
            raise UnprocessableEntity()  # pragma: no cover

    @app.route("/projects/<project_id>/categorisations")
    @app.auth()
    def projects_categorisations(project_id: str):
        """
        Returns Categorisation resources associated with a specific Project resource, specified by its Neutral ID

        :type project_id: str
        :param project_id: neutral ID of a Project resource
        """
        try:
            project = Project.query.filter_by(neutral_id=project_id).one()
            payload = ProjectSchema(
                related_resource="categorisations", many_related=True
            ).dump(project)
            return jsonify(payload)
        except NoResultFound:
            raise NotFound()
        except MultipleResultsFound:  # pragma: no cover
            raise UnprocessableEntity()  # pragma: no cover

    @app.route("/people")
    @app.auth()
    def people_list():
        """
        Returns all People resources

        The response is paginated.
        """
        page = request.args.get("page", type=int)
        if page is None:
            page = 1

        _people = Person.query.paginate(page=page, per_page=app.config["APP_PAGE_SIZE"])
        payload = PersonSchema(
            many=True,
            paginate=True,
            include_data=("organisation", "participation", "participation.project"),
        ).dump(_people)

        return jsonify(payload)

    @app.route("/people/<person_id>")
    @app.auth()
    def people_detail(person_id: str):
        """
        Returns a specific Person resource, specified by its Neutral ID

        :type person_id: str
        :param person_id: neutral ID of a Person resource
        """
        try:
            person = Person.query.filter_by(neutral_id=person_id).one()
            payload = PersonSchema(
                include_data=("organisation", "participation", "participation.project")
            ).dump(person)
            return jsonify(payload)
        except NoResultFound:
            raise NotFound()
        except MultipleResultsFound:  # pragma: no cover
            raise UnprocessableEntity()  # pragma: no cover

    @app.route("/people/<person_id>/relationships/participants")
    @app.auth()
    def people_relationship_participants(person_id: str):
        """
        Returns Participant resource linkages associated with a specific Person resource, specified by its Neutral ID

        :type person_id: str
        :param person_id: neutral ID of a Person resource
        """
        try:
            person = Person.query.filter_by(neutral_id=person_id).one()
            payload = PersonSchema(resource_linkage="participation").dump(person)
            return jsonify(payload)
        except NoResultFound:
            raise NotFound()
        except MultipleResultsFound:  # pragma: no cover
            raise UnprocessableEntity()  # pragma: no cover

    @app.route("/people/<person_id>/relationships/organisations")
    @app.auth()
    def people_relationship_organisations(person_id: str):
        """
        Returns Organisation resource linkages associated with a specific Person resource, specified by its Neutral ID

        :type person_id: str
        :param person_id: neutral ID of a Person resource
        """
        try:
            person = Person.query.filter_by(neutral_id=person_id).one()
            payload = PersonSchema(resource_linkage="organisation").dump(person)
            return jsonify(payload)
        except NoResultFound:
            raise NotFound()
        except MultipleResultsFound:  # pragma: no cover
            raise UnprocessableEntity()  # pragma: no cover

    @app.route("/people/<person_id>/participants")
    @app.auth()
    def people_participants(person_id: str):
        """
        Returns Participant resources associated with a specific Person resource, specified by its Neutral ID

        :type person_id: str
        :param person_id: neutral ID of a Person resource
        """
        try:
            person = Person.query.filter_by(neutral_id=person_id).one()
            payload = PersonSchema(
                related_resource="participation", many_related=True
            ).dump(person)
            return jsonify(payload)
        except NoResultFound:
            raise NotFound()
        except MultipleResultsFound:  # pragma: no cover
            raise UnprocessableEntity()  # pragma: no cover

    @app.route("/people/<person_id>/organisations")
    @app.auth()
    def people_organisations(person_id: str):
        """
        Returns Organisation resources associated with a specific Person resource, specified by its Neutral ID

        :type person_id: str
        :param person_id: neutral ID of a Person resource
        """
        try:
            person = Person.query.filter_by(neutral_id=person_id).one()
            payload = PersonSchema(
                related_resource="organisation", many_related=False
            ).dump(person)
            return jsonify(payload)
        except NoResultFound:
            raise NotFound()
        except MultipleResultsFound:  # pragma: no cover
            raise UnprocessableEntity()  # pragma: no cover

    @app.route("/grants")
    @app.auth()
    def grants_list():
        """
        Returns all Grant resources

        The response is paginated.
        """
        page = request.args.get("page", type=int)
        if page is None:
            page = 1

        _grants = Grant.query.paginate(page=page, per_page=app.config["APP_PAGE_SIZE"])
        payload = GrantSchema(
            many=True,
            paginate=True,
            include_data=("funder", "allocations", "allocations.project"),
        ).dump(_grants)

        return jsonify(payload)

    @app.route("/grants/<grant_id>")
    @app.auth()
    def grants_detail(grant_id: str):
        """
        Returns a specific Grant resource, specified by its Neutral ID

        :type grant_id: str
        :param grant_id: neutral ID of a Grant resource
        """
        try:
            grant = Grant.query.filter_by(neutral_id=grant_id).one()
            payload = GrantSchema(
                include_data=("funder", "allocations", "allocations.project")
            ).dump(grant)
            return jsonify(payload)
        except NoResultFound:
            raise NotFound()
        except MultipleResultsFound:  # pragma: no cover
            raise UnprocessableEntity()  # pragma: no cover

    @app.route("/grants/<grant_id>/relationships/allocations")
    @app.auth()
    def grants_relationship_allocations(grant_id: str):
        """
        Returns Allocation resource linkages associated with a specific Grant resource, specified by its Neutral ID

        :type grant_id: str
        :param grant_id: neutral ID of a Grant resource
        """
        try:
            grant = Grant.query.filter_by(neutral_id=grant_id).one()
            payload = GrantSchema(resource_linkage="allocations").dump(grant)
            return jsonify(payload)
        except NoResultFound:
            raise NotFound()
        except MultipleResultsFound:  # pragma: no cover
            raise UnprocessableEntity()  # pragma: no cover

    @app.route("/grants/<grant_id>/relationships/organisations")
    @app.auth()
    def grants_relationship_organisations(grant_id: str):
        """
        Returns Organisation resource linkages associated with a specific Grant resource, specified by its Neutral ID

        :type grant_id: str
        :param grant_id: neutral ID of a Grant resource
        """
        try:
            grant = Grant.query.filter_by(neutral_id=grant_id).one()
            payload = GrantSchema(resource_linkage="funder").dump(grant)
            return jsonify(payload)
        except NoResultFound:
            raise NotFound()
        except MultipleResultsFound:  # pragma: no cover
            raise UnprocessableEntity()  # pragma: no cover

    @app.route("/grants/<grant_id>/allocations")
    @app.auth()
    def grants_allocations(grant_id: str):
        """
        Returns Allocation resources associated with a specific Grant resource, specified by its Neutral ID

        :type grant_id: str
        :param grant_id: neutral ID of a Grant resource
        """
        try:
            grant = Grant.query.filter_by(neutral_id=grant_id).one()
            payload = GrantSchema(
                related_resource="allocations", many_related=True
            ).dump(grant)
            return jsonify(payload)
        except NoResultFound:
            raise NotFound()
        except MultipleResultsFound:  # pragma: no cover
            raise UnprocessableEntity()  # pragma: no cover

    @app.route("/grants/<grant_id>/organisations")
    @app.auth()
    def grants_organisations(grant_id: str):
        """
        Returns Organisation resources associated with a specific Grant resource, specified by its Neutral ID

        :type grant_id: str
        :param grant_id: neutral ID of a Grant resource
        """
        try:
            grant = Grant.query.filter_by(neutral_id=grant_id).one()
            payload = GrantSchema(related_resource="funder", many_related=False).dump(
                grant
            )
            return jsonify(payload)
        except NoResultFound:
            raise NotFound()
        except MultipleResultsFound:  # pragma: no cover
            raise UnprocessableEntity()  # pragma: no cover

    @app.route("/organisations")
    @app.auth()
    def organisations_list():
        """
        Returns all Organisation resources

        The response is paginated.
        """
        page = request.args.get("page", type=int)
        if page is None:
            page = 1

        _organisations = Organisation.query.paginate(
            page=page, per_page=app.config["APP_PAGE_SIZE"]
        )
        payload = OrganisationSchema(
            many=True,
            paginate=True,
            include_data=(
                "people",
                "people.participation",
                "people.participation.project",
                "grants",
                "grants.allocations",
                "grants.allocations.project",
            ),
        ).dump(_organisations)

        return jsonify(payload)

    @app.route("/organisations/<organisation_id>")
    @app.auth()
    def organisations_detail(organisation_id: str):
        """
        Returns a specific Organisation resource, specified by its Neutral ID

        :type organisation_id: str
        :param organisation_id: neutral ID of a Organisation resource
        """
        try:
            organisation = Organisation.query.filter_by(
                neutral_id=organisation_id
            ).one()
            payload = OrganisationSchema(
                include_data=(
                    "people",
                    "people.participation",
                    "people.participation.project",
                    "grants",
                    "grants.allocations",
                    "grants.allocations.project",
                )
            ).dump(organisation)
            return jsonify(payload)
        except NoResultFound:
            raise NotFound()
        except MultipleResultsFound:  # pragma: no cover
            raise UnprocessableEntity()  # pragma: no cover

    @app.route("/organisations/<organisation_id>/relationships/people")
    @app.auth()
    def organisations_relationship_people(organisation_id: str):
        """
        Returns Person resource linkages associated with a specific Organisation resource, specified by its Neutral ID

        :type organisation_id: str
        :param organisation_id: neutral ID of a Organisation resource
        """
        try:
            organisation = Organisation.query.filter_by(
                neutral_id=organisation_id
            ).one()
            payload = OrganisationSchema(resource_linkage="people").dump(organisation)
            return jsonify(payload)
        except NoResultFound:
            raise NotFound()
        except MultipleResultsFound:  # pragma: no cover
            raise UnprocessableEntity()  # pragma: no cover

    @app.route("/organisations/<organisation_id>/relationships/grants")
    @app.auth()
    def organisations_relationship_grants(organisation_id: str):
        """
        Returns Grant resource linkages associated with a specific Organisation resource, specified by its Neutral ID

        :type organisation_id: str
        :param organisation_id: neutral ID of a Organisation resource
        """
        try:
            organisation = Organisation.query.filter_by(
                neutral_id=organisation_id
            ).one()
            payload = OrganisationSchema(resource_linkage="grants").dump(organisation)
            return jsonify(payload)
        except NoResultFound:
            raise NotFound()
        except MultipleResultsFound:  # pragma: no cover
            raise UnprocessableEntity()  # pragma: no cover

    @app.route("/organisations/<organisation_id>/people")
    @app.auth()
    def organisations_people(organisation_id: str):
        """
        Returns Person resources associated with a specific Organisation resource, specified by its Neutral ID

        :type organisation_id: str
        :param organisation_id: neutral ID of a Organisation resource
        """
        try:
            organisation = Organisation.query.filter_by(
                neutral_id=organisation_id
            ).one()
            payload = OrganisationSchema(
                related_resource="people", many_related=True
            ).dump(organisation)
            return jsonify(payload)
        except NoResultFound:
            raise NotFound()
        except MultipleResultsFound:  # pragma: no cover
            raise UnprocessableEntity()  # pragma: no cover

    @app.route("/organisations/<organisation_id>/grants")
    @app.auth()
    def organisations_grants(organisation_id: str):
        """
        Returns Grant resources associated with a specific Organisation resource, specified by its Neutral ID

        :type organisation_id: str
        :param organisation_id: neutral ID of a Organisation resource
        """
        try:
            organisation = Organisation.query.filter_by(
                neutral_id=organisation_id
            ).one()
            payload = OrganisationSchema(
                related_resource="grants", many_related=True
            ).dump(organisation)
            return jsonify(payload)
        except NoResultFound:
            raise NotFound()
        except MultipleResultsFound:  # pragma: no cover
            raise UnprocessableEntity()  # pragma: no cover

    @app.route("/category-schemes")
    @app.auth()
    def category_schemes_list():
        """
        Returns all CategoryScheme resources

        The response is paginated.
        """
        page = request.args.get("page", type=int)
        if page is None:
            page = 1

        _category_schemes = CategoryScheme.query.paginate(
            page=page, per_page=app.config["APP_PAGE_SIZE"]
        )
        payload = CategorySchemeSchema(
            many=True,
            paginate=True,
            include_data=(
                # 'categories',
                # 'categories.categorisations.project'
            ),
        ).dump(_category_schemes)

        return jsonify(payload)

    @app.route("/category-schemes/<category_scheme_id>")
    @app.auth()
    def category_schemes_detail(category_scheme_id: str):
        """
        Returns a specific CategoryScheme resource, specified by its Neutral ID

        :type category_scheme_id: str
        :param category_scheme_id: neutral ID of a CategoryTerm resource
        """
        try:
            category_scheme = CategoryScheme.query.filter_by(
                neutral_id=category_scheme_id
            ).one()
            payload = CategorySchemeSchema(
                include_data=("categories", "categories.categorisations.project")
            ).dump(category_scheme)
            return jsonify(payload)
        except NoResultFound:
            raise NotFound()
        except MultipleResultsFound:  # pragma: no cover
            raise UnprocessableEntity()  # pragma: no cover

    @app.route("/category-schemes/<category_scheme_id>/relationships/categories")
    @app.auth()
    def category_schemes_relationship_category_terms(category_scheme_id: str):
        """
        Returns CategoryTerm resource linkages associated with a specific CategoryScheme resource, specified by its Neutral
        ID

        :type category_scheme_id: str
        :param category_scheme_id: neutral ID of a CategoryTerm resource
        """
        try:
            category_scheme = CategoryScheme.query.filter_by(
                neutral_id=category_scheme_id
            ).one()
            payload = CategorySchemeSchema(resource_linkage="categories").dump(
                category_scheme
            )
            return jsonify(payload)
        except NoResultFound:
            raise NotFound()
        except MultipleResultsFound:  # pragma: no cover
            raise UnprocessableEntity()  # pragma: no cover

    @app.route("/category-schemes/<category_scheme_id>/categories")
    @app.auth()
    def category_schemes_category_terms(category_scheme_id: str):
        """
        Returns CategoryTerm resources associated with a specific CategoryScheme resource, specified by its Neutral ID

        :type category_scheme_id: str
        :param category_scheme_id: neutral ID of a CategoryTerm resource
        """
        try:
            category_scheme = CategoryScheme.query.filter_by(
                neutral_id=category_scheme_id
            ).one()
            payload = CategorySchemeSchema(
                related_resource="categories", many_related=True
            ).dump(category_scheme)
            return jsonify(payload)
        except NoResultFound:
            raise NotFound()
        except MultipleResultsFound:  # pragma: no cover
            raise UnprocessableEntity()  # pragma: no cover

    @app.route("/categories")
    @app.auth()
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

    @app.route("/categories/<category_term_id>")
    @app.auth()
    def category_terms_detail(category_term_id: str):
        """
        Returns a specific CategoryTerm resource, specified by its Neutral ID

        :type category_term_id: str
        :param category_term_id: neutral ID of a CategoryTerm resource
        """
        try:
            category_term = CategoryTerm.query.filter_by(
                neutral_id=category_term_id
            ).one()
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
        except MultipleResultsFound:  # pragma: no cover
            raise UnprocessableEntity()  # pragma: no cover

    @app.route("/categories/<category_term_id>/relationships/parent-categories")
    @app.auth()
    def category_terms_relationship_parent_category_terms(category_term_id: str):
        """
        Returns parent CategoryTerm resource linkages for a specific CategoryTerm resource, specified by its Neutral ID

        :type category_term_id: str
        :param category_term_id: neutral ID of a CategoryTerm resource
        """
        try:
            category_term = CategoryTerm.query.filter_by(
                neutral_id=category_term_id
            ).one()
            payload = CategoryTermSchema(resource_linkage="parent-category").dump(
                category_term
            )
            return jsonify(payload)
        except NoResultFound:
            raise NotFound()
        except MultipleResultsFound:  # pragma: no cover
            raise UnprocessableEntity()  # pragma: no cover

    @app.route("/categories/<category_term_id>/relationships/category-schemes")
    @app.auth()
    def category_terms_relationship_category_schemes(category_term_id: str):
        """
        Returns CategoryScheme resource linkages associated with a specific CategoryTerm resource, specified by its Neutral
        ID

        :type category_term_id: str
        :param category_term_id: neutral ID of a CategoryTerm resource
        """
        try:
            category_term = CategoryTerm.query.filter_by(
                neutral_id=category_term_id
            ).one()
            payload = CategoryTermSchema(resource_linkage="category-scheme").dump(
                category_term
            )
            return jsonify(payload)
        except NoResultFound:
            raise NotFound()
        except MultipleResultsFound:  # pragma: no cover
            raise UnprocessableEntity()  # pragma: no cover

    @app.route("/categories/<category_term_id>/relationships/categorisations")
    @app.auth()
    def category_terms_relationship_categorisations(category_term_id: str):
        """
        Returns Categorisation resource linkages associated with a specific CategoryTerm resource, specified by its Neutral
        ID

        :type category_term_id: str
        :param category_term_id: neutral ID of a CategoryTerm resource
        """
        try:
            category_term = CategoryTerm.query.filter_by(
                neutral_id=category_term_id
            ).one()
            payload = CategoryTermSchema(resource_linkage="categorisations").dump(
                category_term
            )
            return jsonify(payload)
        except NoResultFound:
            raise NotFound()
        except MultipleResultsFound:  # pragma: no cover
            raise UnprocessableEntity()  # pragma: no cover

    @app.route("/categories/<category_term_id>/parent-categories")
    @app.auth()
    def category_terms_parent_category_terms(category_term_id: str):
        """
        Returns parent CategoryTerm resources associated with a specific CategoryTerm resource, specified by its Neutral ID

        :type category_term_id: str
        :param category_term_id: neutral ID of a CategoryTerm resource
        """
        try:
            category_term = CategoryTerm.query.filter_by(
                neutral_id=category_term_id
            ).one()
            payload = CategoryTermSchema(
                related_resource="parent_category", many_related=False
            ).dump(category_term)
            return jsonify(payload)
        except NoResultFound:
            raise NotFound()
        except MultipleResultsFound:  # pragma: no cover
            raise UnprocessableEntity()  # pragma: no cover

    @app.route("/categories/<category_term_id>/category-schemes")
    @app.auth()
    def category_terms_category_schemes(category_term_id: str):
        """
        Returns CategoryScheme resources associated with a specific CategoryTerm resource, specified by its Neutral ID

        :type category_term_id: str
        :param category_term_id: neutral ID of a CategoryTerm resource
        """
        try:
            category_term = CategoryTerm.query.filter_by(
                neutral_id=category_term_id
            ).one()
            payload = CategoryTermSchema(
                related_resource="category_scheme", many_related=False
            ).dump(category_term)
            return jsonify(payload)
        except NoResultFound:
            raise NotFound()
        except MultipleResultsFound:  # pragma: no cover
            raise UnprocessableEntity()  # pragma: no cover

    @app.route("/categories/<category_term_id>/categorisations")
    @app.auth()
    def category_terms_categorisations(category_term_id: str):
        """
        Returns Categorisation resources associated with a specific CategoryTerm resource, specified by its Neutral ID

        :type category_term_id: str
        :param category_term_id: neutral ID of a CategoryTerm resource
        """
        try:
            category_term = CategoryTerm.query.filter_by(
                neutral_id=category_term_id
            ).one()
            payload = CategoryTermSchema(
                related_resource="categorisations", many_related=True
            ).dump(category_term)
            return jsonify(payload)
        except NoResultFound:
            raise NotFound()
        except MultipleResultsFound:  # pragma: no cover
            raise UnprocessableEntity()  # pragma: no cover

    @app.route("/participants")
    @app.auth()
    def participants_list():
        """
        Returns all Participant resources (People, Project association)

        The response is paginated.
        """
        page = request.args.get("page", type=int)
        if page is None:
            page = 1

        _participants = Participant.query.paginate(
            page=page, per_page=app.config["APP_PAGE_SIZE"]
        )
        payload = ParticipantSchema(
            many=True, paginate=True, include_data=("project", "person")
        ).dump(_participants)

        return jsonify(payload)

    @app.route("/participants/<participant_id>")
    @app.auth()
    def participants_detail(participant_id: str):
        """
        Returns a specific Participant resource, specified by its Neutral ID

        :type participant_id: str
        :param participant_id: neutral ID of a Participant resource
        """
        try:
            participant = Participant.query.filter_by(neutral_id=participant_id).one()
            payload = ParticipantSchema(include_data=("project", "person")).dump(
                participant
            )
            return jsonify(payload)
        except NoResultFound:
            raise NotFound()
        except MultipleResultsFound:  # pragma: no cover
            raise UnprocessableEntity()  # pragma: no cover

    @app.route("/participants/<participant_id>/relationships/projects")
    @app.auth()
    def participants_relationship_projects(participant_id: str):
        """
        Returns Project resource linkages associated with a specific Participant resource, specified by its Neutral ID

        :type participant_id: str
        :param participant_id: neutral ID of a Participant resource
        """
        try:
            participant = Participant.query.filter_by(neutral_id=participant_id).one()
            payload = ParticipantSchema(resource_linkage="project").dump(participant)
            return jsonify(payload)
        except NoResultFound:
            raise NotFound()
        except MultipleResultsFound:  # pragma: no cover
            raise UnprocessableEntity()  # pragma: no cover

    @app.route("/participants/<participant_id>/relationships/people")
    @app.auth()
    def participants_relationship_people(participant_id: str):
        """
        Returns People resource linkages associated with a specific Participant resource, specified by its Neutral ID

        :type participant_id: str
        :param participant_id: neutral ID of a Participant resource
        """
        try:
            participant = Participant.query.filter_by(neutral_id=participant_id).one()
            payload = ParticipantSchema(resource_linkage="person").dump(participant)
            return jsonify(payload)
        except NoResultFound:
            raise NotFound()
        except MultipleResultsFound:  # pragma: no cover
            raise UnprocessableEntity()  # pragma: no cover

    @app.route("/participants/<participant_id>/projects")
    @app.auth()
    def participants_projects(participant_id: str):
        """
        Returns the Project resource associated with a specific Participant resource, specified by its Neutral ID

        :type participant_id: str
        :param participant_id: neutral ID of a Participant resource
        """
        try:
            participant = Participant.query.filter_by(neutral_id=participant_id).one()
            payload = ParticipantSchema(
                related_resource="project", many_related=False
            ).dump(participant)
            return jsonify(payload)
        except NoResultFound:
            raise NotFound()
        except MultipleResultsFound:  # pragma: no cover
            raise UnprocessableEntity()  # pragma: no cover

    @app.route("/participants/<participant_id>/people")
    @app.auth()
    def participants_people(participant_id: str):
        """
        Returns the People resource associated with a specific Participant resource, specified by its Neutral ID

        :type participant_id: str
        :param participant_id: neutral ID of a Participant resource
        """
        try:
            participant = Participant.query.filter_by(neutral_id=participant_id).one()
            payload = ParticipantSchema(
                related_resource="person", many_related=False
            ).dump(participant)
            return jsonify(payload)
        except NoResultFound:
            raise NotFound()
        except MultipleResultsFound:  # pragma: no cover
            raise UnprocessableEntity()  # pragma: no cover

    @app.route("/allocations")
    @app.auth()
    def allocations_list():
        """
        Returns all Allocation resources (Grant, Project association)

        The response is paginated.
        """
        page = request.args.get("page", type=int)
        if page is None:
            page = 1

        _allocations = Allocation.query.paginate(
            page=page, per_page=app.config["APP_PAGE_SIZE"]
        )
        payload = AllocationSchema(
            many=True, paginate=True, include_data=("project", "grant")
        ).dump(_allocations)

        return jsonify(payload)

    @app.route("/allocations/<allocation_id>")
    @app.auth()
    def allocations_detail(allocation_id: str):
        """
        Returns a specific Allocation resource, specified by its Neutral ID

        :type allocation_id: str
        :param allocation_id: neutral ID of a Allocation resource
        """
        try:
            allocation = Allocation.query.filter_by(neutral_id=allocation_id).one()
            payload = AllocationSchema(include_data=("project", "grant")).dump(
                allocation
            )
            return jsonify(payload)
        except NoResultFound:
            raise NotFound()
        except MultipleResultsFound:  # pragma: no cover
            raise UnprocessableEntity()  # pragma: no cover

    @app.route("/allocations/<allocation_id>/relationships/projects")
    @app.auth()
    def allocations_relationship_projects(allocation_id: str):
        """
        Returns Project resource linkages associated with a specific Allocation resource, specified by its Neutral ID

        :type allocation_id: str
        :param allocation_id: neutral ID of a Allocation resource
        """
        try:
            allocation = Allocation.query.filter_by(neutral_id=allocation_id).one()
            payload = AllocationSchema(resource_linkage="project").dump(allocation)
            return jsonify(payload)
        except NoResultFound:
            raise NotFound()
        except MultipleResultsFound:  # pragma: no cover
            raise UnprocessableEntity()  # pragma: no cover

    @app.route("/allocations/<allocation_id>/relationships/grants")
    @app.auth()
    def allocations_relationship_grants(allocation_id: str):
        """
        Returns Grant resource linkages associated with a specific Allocation resource, specified by its Neutral ID

        :type allocation_id: str
        :param allocation_id: neutral ID of a Allocation resource
        """
        try:
            allocation = Allocation.query.filter_by(neutral_id=allocation_id).one()
            payload = AllocationSchema(resource_linkage="grant").dump(allocation)
            return jsonify(payload)
        except NoResultFound:
            raise NotFound()
        except MultipleResultsFound:  # pragma: no cover
            raise UnprocessableEntity()  # pragma: no cover

    @app.route("/allocations/<allocation_id>/projects")
    @app.auth()
    def allocations_projects(allocation_id: str):
        """
        Returns the Project resource associated with a specific Allocation resource, specified by its Neutral ID

        :type allocation_id: str
        :param allocation_id: neutral ID of a Allocation resource
        """
        try:
            allocation = Allocation.query.filter_by(neutral_id=allocation_id).one()
            payload = AllocationSchema(
                related_resource="project", many_related=False
            ).dump(allocation)
            return jsonify(payload)
        except NoResultFound:
            raise NotFound()
        except MultipleResultsFound:  # pragma: no cover
            raise UnprocessableEntity()  # pragma: no cover

    @app.route("/allocations/<allocation_id>/grants")
    @app.auth()
    def allocations_grants(allocation_id: str):
        """
        Returns the People resource associated with a specific Allocation resource, specified by its Neutral ID

        :type allocation_id: str
        :param allocation_id: neutral ID of a Allocation resource
        """
        try:
            allocation = Allocation.query.filter_by(neutral_id=allocation_id).one()
            payload = AllocationSchema(
                related_resource="grant", many_related=False
            ).dump(allocation)
            return jsonify(payload)
        except NoResultFound:
            raise NotFound()
        except MultipleResultsFound:  # pragma: no cover
            raise UnprocessableEntity()  # pragma: no cover

    @app.route("/categorisations")
    @app.auth()
    def categorisations_list():
        """
        Returns all Categorisation resources

        The response is paginated.
        """
        page = request.args.get("page", type=int)
        if page is None:
            page = 1

        _categorisations = Categorisation.query.paginate(
            page=page, per_page=app.config["APP_PAGE_SIZE"]
        )
        payload = CategorisationSchema(
            many=True,
            paginate=True,
            include_data=(
                "project",
                "category",
                "category.parent_category",
                "category.category_scheme",
            ),
        ).dump(_categorisations)

        return jsonify(payload)

    @app.route("/categorisations/<categorisation_id>")
    @app.auth()
    def categorisations_detail(categorisation_id: str):
        """
        Returns a specific Categorisation resource, specified by its Neutral ID

        :type categorisation_id: str
        :param categorisation_id: neutral ID of a Categorisation resource
        """
        try:
            categorisation = Categorisation.query.filter_by(
                neutral_id=categorisation_id
            ).one()
            payload = CategorisationSchema(
                include_data=(
                    "project",
                    "category",
                    "category.parent_category",
                    "category.category_scheme",
                )
            ).dump(categorisation)
            return jsonify(payload)
        except NoResultFound:
            raise NotFound()
        except MultipleResultsFound:  # pragma: no cover
            raise UnprocessableEntity()  # pragma: no cover

    @app.route("/categorisations/<categorisation_id>/relationships/projects")
    @app.auth()
    def categorisations_relationship_projects(categorisation_id: str):
        """
        Returns Project resource linkages associated with a specific Categorisation resource, specified by its Neutral ID

        :type categorisation_id: str
        :param categorisation_id: neutral ID of a CategoryTerm resource
        """
        try:
            categorisation = Categorisation.query.filter_by(
                neutral_id=categorisation_id
            ).one()
            payload = CategorisationSchema(resource_linkage="project").dump(
                categorisation
            )
            return jsonify(payload)
        except NoResultFound:
            raise NotFound()
        except MultipleResultsFound:  # pragma: no cover
            raise UnprocessableEntity()  # pragma: no cover

    @app.route("/categorisations/<categorisation_id>/relationships/categories")
    @app.auth()
    def categorisations_relationship_category_terms(categorisation_id: str):
        """
        Returns CategoryTerm resource linkages associated with a specific Categorisation resource, specified by its Neutral
        ID

        :type categorisation_id: str
        :param categorisation_id: neutral ID of a CategoryTerm resource
        """
        try:
            categorisation = Categorisation.query.filter_by(
                neutral_id=categorisation_id
            ).one()
            payload = CategorisationSchema(resource_linkage="category").dump(
                categorisation
            )
            return jsonify(payload)
        except NoResultFound:
            raise NotFound()
        except MultipleResultsFound:  # pragma: no cover
            raise UnprocessableEntity()  # pragma: no cover

    @app.route("/categorisations/<categorisation_id>/projects")
    @app.auth()
    def categorisations_projects(categorisation_id: str):
        """
        Returns Project resources associated with a specific Categorisation resource, specified by its Neutral ID

        :type categorisation_id: str
        :param categorisation_id: neutral ID of a CategoryTerm resource
        """
        try:
            categorisation = Categorisation.query.filter_by(
                neutral_id=categorisation_id
            ).one()
            payload = CategorisationSchema(
                related_resource="project", many_related=False
            ).dump(categorisation)
            return jsonify(payload)
        except NoResultFound:
            raise NotFound()
        except MultipleResultsFound:  # pragma: no cover
            raise UnprocessableEntity()  # pragma: no cover

    @app.route("/categorisations/<categorisation_id>/categories")
    @app.auth()
    def categorisations_category_terms(categorisation_id: str):
        """
        Returns CategoryTerm resources associated with a specific Categorisation resource, specified by its Neutral ID

        :type categorisation_id: str
        :param categorisation_id: neutral ID of a CategoryTerm resource
        """
        try:
            categorisation = Categorisation.query.filter_by(
                neutral_id=categorisation_id
            ).one()
            payload = CategorisationSchema(
                related_resource="category", many_related=False
            ).dump(categorisation)
            return jsonify(payload)
        except NoResultFound:
            raise NotFound()
        except MultipleResultsFound:  # pragma: no cover
            raise UnprocessableEntity()  # pragma: no cover

    # Return create_app()
    return app
