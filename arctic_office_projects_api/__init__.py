import os

import sentry_sdk

from flask import Flask, jsonify, request
from flask_entra_auth.resource_protector import FlaskEntraAuth
from flask.logging import default_handler
from werkzeug.middleware.proxy_fix import ProxyFix

# from flask_reverse_proxy_fix.middleware import ReverseProxyPrefixFix
from flask_request_id_header.middleware import RequestID

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

# noinspection PyPackageRequirements
from werkzeug.exceptions import (
    BadRequest,
    NotFound,
    InternalServerError,
    UnprocessableEntity,
)

from config import config
from arctic_office_projects_api.logging import RequestFormatter
from arctic_office_projects_api.extensions import db
from arctic_office_projects_api.errors import (
    error_handler_generic_bad_request,
    error_handler_generic_not_found,
    error_handler_generic_internal_server_error,
    error_handler_generic_unprocessable_entity,
)
from arctic_office_projects_api.commands import seeding_cli_group, importing_cli_group
from arctic_office_projects_api.routes import index_route, healthcheck_canary_route

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

from arctic_office_projects_api.utils import conditional_decorator


auth = FlaskEntraAuth()


def create_app(config_name):
    app = Flask(__name__)

    # Config
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI") or None

    auth = FlaskEntraAuth()
    auth.init_app(app)

    db.init_app(app)

    # # Middleware / Wrappers
    if app.config["APP_ENABLE_PROXY_FIX"]:
        app.wsgi_app = ProxyFix(
            app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1
        )
        # ReverseProxyPrefixFix(app)
    if app.config["APP_ENABLE_REQUEST_ID"]:
        RequestID(app)
    if app.config["APP_ENABLE_SENTRY"]:
        sentry_sdk.init(**app.config["SENTRY_CONFIG"])  # pragma: no cover

    # Logging
    formatter = RequestFormatter(
        "[%(asctime)s] [%(levelname)s] [%(request_id)s] [%(url)s]: %(message)s"
    )
    default_handler.setFormatter(formatter)
    default_handler.setLevel(app.config["LOGGING_LEVEL"])

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
        "/meta/health/canary",
        "canary_health_check",
        healthcheck_canary_route,
        methods=["get", "options"],
    )

    is_testing = app.config.get("TESTING")

    # Resources
    @app.route("/projects")
    @conditional_decorator(app.auth(), is_testing)
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
    @conditional_decorator(app.auth(), is_testing)
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
        except MultipleResultsFound:
            raise UnprocessableEntity()

    @app.route("/projects/<project_id>/relationships/participants")
    @conditional_decorator(app.auth(), is_testing)
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
        except MultipleResultsFound:
            raise UnprocessableEntity()

    @app.route("/projects/<project_id>/relationships/allocations")
    @conditional_decorator(app.auth(), is_testing)
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
        except MultipleResultsFound:
            raise UnprocessableEntity()

    @app.route("/projects/<project_id>/participants")
    @conditional_decorator(app.auth(), is_testing)
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
        except MultipleResultsFound:
            raise UnprocessableEntity()

    @app.route("/projects/<project_id>/allocations")
    @conditional_decorator(app.auth(), is_testing)
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
        except MultipleResultsFound:
            raise UnprocessableEntity()

    @app.route("/projects/<project_id>/relationships/categorisations")
    @conditional_decorator(app.auth(), is_testing)
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
        except MultipleResultsFound:
            raise UnprocessableEntity()

    @app.route("/projects/<project_id>/categorisations")
    @conditional_decorator(app.auth(), is_testing)
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
        except MultipleResultsFound:
            raise UnprocessableEntity()

    @app.route("/people")
    @conditional_decorator(app.auth(), is_testing)
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
    @conditional_decorator(app.auth(), is_testing)
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
        except MultipleResultsFound:
            raise UnprocessableEntity()

    @app.route("/people/<person_id>/relationships/participants")
    @conditional_decorator(app.auth(), is_testing)
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
        except MultipleResultsFound:
            raise UnprocessableEntity()

    @app.route("/people/<person_id>/relationships/organisations")
    @conditional_decorator(app.auth(), is_testing)
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
        except MultipleResultsFound:
            raise UnprocessableEntity()

    @app.route("/people/<person_id>/participants")
    @conditional_decorator(app.auth(), is_testing)
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
        except MultipleResultsFound:
            raise UnprocessableEntity()

    @app.route("/people/<person_id>/organisations")
    @conditional_decorator(app.auth(), is_testing)
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
        except MultipleResultsFound:
            raise UnprocessableEntity()

    @app.route("/grants")
    @conditional_decorator(app.auth(), is_testing)
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
    @conditional_decorator(app.auth(), is_testing)
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
        except MultipleResultsFound:
            raise UnprocessableEntity()

    @app.route("/grants/<grant_id>/relationships/allocations")
    @conditional_decorator(app.auth(), is_testing)
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
        except MultipleResultsFound:
            raise UnprocessableEntity()

    @app.route("/grants/<grant_id>/relationships/organisations")
    @conditional_decorator(app.auth(), is_testing)
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
        except MultipleResultsFound:
            raise UnprocessableEntity()

    @app.route("/grants/<grant_id>/allocations")
    @conditional_decorator(app.auth(), is_testing)
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
        except MultipleResultsFound:
            raise UnprocessableEntity()

    @app.route("/grants/<grant_id>/organisations")
    @conditional_decorator(app.auth(), is_testing)
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
        except MultipleResultsFound:
            raise UnprocessableEntity()

    @app.route("/organisations")
    @conditional_decorator(app.auth(), is_testing)
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
    @conditional_decorator(app.auth(), is_testing)
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
        except MultipleResultsFound:
            raise UnprocessableEntity()

    @app.route("/organisations/<organisation_id>/relationships/people")
    @conditional_decorator(app.auth(), is_testing)
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
        except MultipleResultsFound:
            raise UnprocessableEntity()

    @app.route("/organisations/<organisation_id>/relationships/grants")
    @conditional_decorator(app.auth(), is_testing)
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
        except MultipleResultsFound:
            raise UnprocessableEntity()

    @app.route("/organisations/<organisation_id>/people")
    @conditional_decorator(app.auth(), is_testing)
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
        except MultipleResultsFound:
            raise UnprocessableEntity()

    @app.route("/organisations/<organisation_id>/grants")
    @conditional_decorator(app.auth(), is_testing)
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
        except MultipleResultsFound:
            raise UnprocessableEntity()

    @app.route("/category-schemes")
    @conditional_decorator(app.auth(), is_testing)
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
    @conditional_decorator(app.auth(), is_testing)
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
        except MultipleResultsFound:
            raise UnprocessableEntity()

    @app.route("/category-schemes/<category_scheme_id>/relationships/categories")
    @conditional_decorator(app.auth(), is_testing)
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
        except MultipleResultsFound:
            raise UnprocessableEntity()

    @app.route("/category-schemes/<category_scheme_id>/categories")
    @conditional_decorator(app.auth(), is_testing)
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
        except MultipleResultsFound:
            raise UnprocessableEntity()

    @app.route("/categories")
    @conditional_decorator(app.auth(), is_testing)
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
    @conditional_decorator(app.auth(), is_testing)
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
        except MultipleResultsFound:
            raise UnprocessableEntity()

    @app.route("/categories/<category_term_id>/relationships/parent-categories")
    @conditional_decorator(app.auth(), is_testing)
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
        except MultipleResultsFound:
            raise UnprocessableEntity()

    @app.route("/categories/<category_term_id>/relationships/category-schemes")
    @conditional_decorator(app.auth(), is_testing)
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
        except MultipleResultsFound:
            raise UnprocessableEntity()

    @app.route("/categories/<category_term_id>/relationships/categorisations")
    @conditional_decorator(app.auth(), is_testing)
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
        except MultipleResultsFound:
            raise UnprocessableEntity()

    @app.route("/categories/<category_term_id>/parent-categories")
    @conditional_decorator(app.auth(), is_testing)
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
        except MultipleResultsFound:
            raise UnprocessableEntity()

    @app.route("/categories/<category_term_id>/category-schemes")
    @conditional_decorator(app.auth(), is_testing)
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
        except MultipleResultsFound:
            raise UnprocessableEntity()

    @app.route("/categories/<category_term_id>/categorisations")
    @conditional_decorator(app.auth(), is_testing)
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
        except MultipleResultsFound:
            raise UnprocessableEntity()

    @app.route("/participants")
    @conditional_decorator(app.auth(), is_testing)
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
    @conditional_decorator(app.auth(), is_testing)
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
        except MultipleResultsFound:
            raise UnprocessableEntity()

    @app.route("/participants/<participant_id>/relationships/projects")
    @conditional_decorator(app.auth(), is_testing)
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
        except MultipleResultsFound:
            raise UnprocessableEntity()

    @app.route("/participants/<participant_id>/relationships/people")
    @conditional_decorator(app.auth(), is_testing)
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
        except MultipleResultsFound:
            raise UnprocessableEntity()

    @app.route("/participants/<participant_id>/projects")
    @conditional_decorator(app.auth(), is_testing)
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
        except MultipleResultsFound:
            raise UnprocessableEntity()

    @app.route("/participants/<participant_id>/people")
    @conditional_decorator(app.auth(), is_testing)
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
        except MultipleResultsFound:
            raise UnprocessableEntity()

    @app.route("/allocations")
    @conditional_decorator(app.auth(), is_testing)
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
    @conditional_decorator(app.auth(), is_testing)
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
        except MultipleResultsFound:
            raise UnprocessableEntity()

    @app.route("/allocations/<allocation_id>/relationships/projects")
    @conditional_decorator(app.auth(), is_testing)
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
        except MultipleResultsFound:
            raise UnprocessableEntity()

    @app.route("/allocations/<allocation_id>/relationships/grants")
    @conditional_decorator(app.auth(), is_testing)
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
        except MultipleResultsFound:
            raise UnprocessableEntity()

    @app.route("/allocations/<allocation_id>/projects")
    @conditional_decorator(app.auth(), is_testing)
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
        except MultipleResultsFound:
            raise UnprocessableEntity()

    @app.route("/allocations/<allocation_id>/grants")
    @conditional_decorator(app.auth(), is_testing)
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
        except MultipleResultsFound:
            raise UnprocessableEntity()

    @app.route("/categorisations")
    @conditional_decorator(app.auth(), is_testing)
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
    @conditional_decorator(app.auth(), is_testing)
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
        except MultipleResultsFound:
            raise UnprocessableEntity()

    @app.route("/categorisations/<categorisation_id>/relationships/projects")
    @conditional_decorator(app.auth(), is_testing)
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
        except MultipleResultsFound:
            raise UnprocessableEntity()

    @app.route("/categorisations/<categorisation_id>/relationships/categories")
    @conditional_decorator(app.auth(), is_testing)
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
        except MultipleResultsFound:
            raise UnprocessableEntity()

    @app.route("/categorisations/<categorisation_id>/projects")
    @conditional_decorator(app.auth(), is_testing)
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
        except MultipleResultsFound:
            raise UnprocessableEntity()

    @app.route("/categorisations/<categorisation_id>/categories")
    @conditional_decorator(app.auth(), is_testing)
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
        except MultipleResultsFound:
            raise UnprocessableEntity()

    # Return create_app()
    return app
