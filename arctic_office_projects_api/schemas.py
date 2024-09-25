# noinspection PyPackageRequirements
from marshmallow import fields

from arctic_office_projects_api.schemas_extension import (
    Schema,
    Relationship,
    DateRangeField,
    EnumStrField,
    EnumDictField,
    CurrencyField,
)
from arctic_office_projects_api.models import CategoryTerm


class ProjectSchema(Schema):
    """
    Represents information about a research project
    """

    id = fields.String(attribute="neutral_id", dump_only=True, required=True)
    title = fields.String(dump_only=True, required=True)
    acronym = fields.String(dump_only=True)
    abstract = fields.String(dump_only=True)
    website = fields.String(dump_only=True)
    lead_project = fields.String(dump_only=True, required=True)
    # noinspection PyTypeChecker
    publications = fields.List(fields.String, dump_only=True)
    access_duration = DateRangeField(dump_only=True, required=True)
    project_duration = DateRangeField(dump_only=True, required=True)
    country = EnumDictField(dump_only=True)

    participants = Relationship(
        self_view="projects_relationship_participants",
        self_view_kwargs={"project_id": "<neutral_id>"},
        related_view="projects_participants",
        related_view_kwargs={"project_id": "<neutral_id>"},
        id_field="neutral_id",
        many=True,
        include_resource_linkage=True,
        type_="participants",
        schema="ParticipantSchema",
    )

    allocations = Relationship(
        self_view="projects_relationship_allocations",
        self_view_kwargs={"project_id": "<neutral_id>"},
        related_view="projects_allocations",
        related_view_kwargs={"project_id": "<neutral_id>"},
        id_field="neutral_id",
        many=True,
        include_resource_linkage=True,
        type_="allocations",
        schema="AllocationSchema",
    )

    categorisations = Relationship(
        self_view="projects_relationship_categorisations",
        self_view_kwargs={"project_id": "<neutral_id>"},
        related_view="projects_categorisations",
        related_view_kwargs={"project_id": "<neutral_id>"},
        id_field="neutral_id",
        many=True,
        include_resource_linkage=True,
        type_="categorisations",
        schema="CategorisationSchema",
    )

    class Meta(Schema.Meta):
        type_ = "projects"
        self_view = "projects_detail"
        self_view_kwargs = {"project_id": "<id>"}
        self_view_many = "projects_list"


class ParticipantSchema(Schema):
    id = fields.String(attribute="neutral_id", dump_only=True, required=True)
    role = EnumDictField(dump_only=True, required=True)

    project = Relationship(
        self_view="participants_relationship_projects",
        self_view_kwargs={"participant_id": "<neutral_id>"},
        related_view="participants_projects",
        related_view_kwargs={"participant_id": "<neutral_id>"},
        id_field="project.neutral_id",
        many=False,
        include_resource_linkage=True,
        type_="projects",
        schema="ProjectSchema",
    )

    person = Relationship(
        self_view="participants_relationship_people",
        self_view_kwargs={"participant_id": "<neutral_id>"},
        related_view="participants_people",
        related_view_kwargs={"participant_id": "<neutral_id>"},
        id_field="person.neutral_id",
        many=False,
        include_resource_linkage=True,
        type_="people",
        schema="PersonSchema",
    )

    class Meta(Schema.Meta):
        type_ = "participants"
        self_view = "participants_detail"
        self_view_kwargs = {"participant_id": "<id>"}
        self_view_many = "participants_list"


class PersonSchema(Schema):
    id = fields.String(attribute="neutral_id", dump_only=True, required=True)
    first_name = fields.String(dump_only=True)
    last_name = fields.String(dump_only=True)
    orcid_id = fields.String(dump_only=True)
    avatar_url = fields.String(attribute="logo_url", dump_only=True)

    organisation = Relationship(
        self_view="people_relationship_organisations",
        self_view_kwargs={"person_id": "<neutral_id>"},
        related_view="people_organisations",
        related_view_kwargs={"person_id": "<neutral_id>"},
        id_field="neutral_id",
        many=False,
        include_resource_linkage=True,
        type_="organisations",
        schema="OrganisationSchema",
    )

    participation = Relationship(
        self_view="people_relationship_participants",
        self_view_kwargs={"person_id": "<neutral_id>"},
        related_view="people_participants",
        related_view_kwargs={"person_id": "<neutral_id>"},
        id_field="neutral_id",
        many=True,
        include_resource_linkage=True,
        type_="participants",
        schema="ParticipantSchema",
    )

    class Meta(Schema.Meta):
        type_ = "people"
        self_view = "people_detail"
        self_view_kwargs = {"person_id": "<id>"}
        self_view_many = "people_list"


class GrantSchema(Schema):
    id = fields.String(attribute="neutral_id", dump_only=True, required=True)
    reference = fields.String(dump_only=True, required=True)
    title = fields.String(dump_only=True, required=True)
    abstract = fields.String(dump_only=True)
    website = fields.String(dump_only=True)
    lead_project = fields.String(dump_only=True, required=True)
    # noinspection PyTypeChecker
    publications = fields.List(fields.String, dump_only=True)
    duration = DateRangeField(dump_only=True, required=True)
    status = EnumStrField(dump_only=True, required=True)
    total_funds = CurrencyField(
        dump_only=True, metadata={"currency": "total_funds_currency"}
    )

    funder = Relationship(
        self_view="grants_relationship_organisations",
        self_view_kwargs={"grant_id": "<neutral_id>"},
        related_view="grants_organisations",
        related_view_kwargs={"grant_id": "<neutral_id>"},
        id_field="neutral_id",
        many=False,
        include_resource_linkage=True,
        type_="organisations",
        schema="OrganisationSchema",
    )

    allocations = Relationship(
        self_view="grants_relationship_allocations",
        self_view_kwargs={"grant_id": "<neutral_id>"},
        related_view="grants_allocations",
        related_view_kwargs={"grant_id": "<neutral_id>"},
        id_field="neutral_id",
        many=True,
        include_resource_linkage=True,
        type_="allocations",
        schema="AllocationSchema",
    )

    class Meta(Schema.Meta):
        type_ = "grants"
        self_view = "grants_detail"
        self_view_kwargs = {"grant_id": "<id>"}
        self_view_many = "grants_list"


class AllocationSchema(Schema):
    id = fields.String(attribute="neutral_id", dump_only=True, required=True)

    project = Relationship(
        self_view="allocations_relationship_projects",
        self_view_kwargs={"allocation_id": "<neutral_id>"},
        related_view="allocations_projects",
        related_view_kwargs={"allocation_id": "<neutral_id>"},
        id_field="project.neutral_id",
        many=False,
        include_resource_linkage=True,
        type_="projects",
        schema="ProjectSchema",
    )

    grant = Relationship(
        self_view="allocations_relationship_grants",
        self_view_kwargs={"allocation_id": "<neutral_id>"},
        related_view="allocations_grants",
        related_view_kwargs={"allocation_id": "<neutral_id>"},
        id_field="grant.neutral_id",
        many=False,
        include_resource_linkage=True,
        type_="grants",
        schema="GrantSchema",
    )

    class Meta(Schema.Meta):
        type_ = "allocations"
        self_view = "allocations_detail"
        self_view_kwargs = {"allocation_id": "<id>"}
        self_view_many = "allocations_list"


class OrganisationSchema(Schema):
    id = fields.String(attribute="neutral_id", dump_only=True, required=True)
    grid_identifier = fields.String(dump_only=True)
    ror_identifier = fields.String(dump_only=True)
    name = fields.String(dump_only=True, required=True)
    acronym = fields.String(dump_only=True)
    website = fields.String(dump_only=True)
    logo_url = fields.String(dump_only=True)

    people = Relationship(
        self_view="organisations_relationship_people",
        self_view_kwargs={"organisation_id": "<neutral_id>"},
        related_view="organisations_people",
        related_view_kwargs={"organisation_id": "<neutral_id>"},
        id_field="neutral_id",
        many=True,
        include_resource_linkage=True,
        type_="people",
        schema="PersonSchema",
    )

    grants = Relationship(
        self_view="organisations_relationship_grants",
        self_view_kwargs={"organisation_id": "<neutral_id>"},
        related_view="organisations_grants",
        related_view_kwargs={"organisation_id": "<neutral_id>"},
        id_field="neutral_id",
        many=True,
        include_resource_linkage=True,
        type_="grants",
        schema="GrantSchema",
    )

    class Meta(Schema.Meta):
        type_ = "organisations"
        self_view = "organisations_detail"
        self_view_kwargs = {"organisation_id": "<id>"}
        self_view_many = "organisations_list"


class CategorySchemeSchema(Schema):
    id = fields.String(attribute="neutral_id", dump_only=True, required=True)
    name = fields.String(dump_only=True, required=True)
    acronym = fields.String(dump_only=True, required=False)
    description = fields.String(dump_only=True, required=False)
    version = fields.String(dump_only=True, required=False)
    revision = fields.String(dump_only=True, required=False)

    categories = Relationship(
        attribute="category_terms",
        self_view="category_schemes_relationship_category_terms",
        self_view_kwargs={"category_scheme_id": "<neutral_id>"},
        related_view="category_schemes_category_terms",
        related_view_kwargs={"category_scheme_id": "<neutral_id>"},
        id_field="neutral_id",
        many=True,
        include_resource_linkage=True,
        type_="categories",
        schema="CategoryTermSchema",
    )

    class Meta(Schema.Meta):
        type_ = "category-schemes"
        self_view = "category_schemes_detail"
        self_view_kwargs = {"category_scheme_id": "<id>"}
        self_view_many = "category_schemes_list"


class CategoryTermSchema(Schema):
    id = fields.String(attribute="neutral_id", dump_only=True, required=True)
    scheme = fields.Method("scheme_class", dump_only=True, required=True)
    concept = fields.String(
        attribute="scheme_identifier", dump_only=True, required=True
    )
    title = fields.String(attribute="name", dump_only=True, required=True)
    notation = fields.String(
        attribute="scheme_notation", dump_only=True, required=False
    )
    # noinspection PyTypeChecker
    aliases = fields.List(fields.String, dump_only=True, required=False)
    # noinspection PyTypeChecker
    definitions = fields.List(fields.String, dump_only=True, required=False)
    # noinspection PyTypeChecker
    examples = fields.List(fields.String, dump_only=True, required=False)
    # noinspection PyTypeChecker
    notes = fields.List(fields.String, dump_only=True, required=False)
    # noinspection PyTypeChecker
    scope_notes = fields.List(fields.String, dump_only=True, required=False)

    # noinspection PyMethodMayBeStatic
    def scheme_class(self, obj: CategoryTerm) -> str:
        """
        Returns the identifier of the category term's schema (i.e. SKOS:inScheme)

        :type obj: CategoryTerm
        :param obj: an CategoryTerm model instance representing the category term being manipulated

        :rtype str
        :return: identifier of the category term's schema
        """
        return obj.category_scheme.namespace

    parent_category = Relationship(
        attribute="parent_category_term",
        self_view="category_terms_relationship_parent_category_terms",
        self_view_kwargs={"category_term_id": "<neutral_id>"},
        related_view="category_terms_parent_category_terms",
        related_view_kwargs={"category_term_id": "<neutral_id>"},
        id_field="neutral_id",
        many=False,
        include_resource_linkage=True,
        type_="categories",
        schema="ParentCategoryTermSchema",
    )

    category_scheme = Relationship(
        self_view="category_terms_relationship_category_schemes",
        self_view_kwargs={"category_term_id": "<neutral_id>"},
        related_view="category_terms_category_schemes",
        related_view_kwargs={"category_term_id": "<neutral_id>"},
        id_field="neutral_id",
        many=False,
        include_resource_linkage=True,
        type_="category-schemes",
        schema="CategorySchemeSchema",
    )

    categorisations = Relationship(
        self_view="category_terms_relationship_categorisations",
        self_view_kwargs={"category_term_id": "<neutral_id>"},
        related_view="category_terms_categorisations",
        related_view_kwargs={"category_term_id": "<neutral_id>"},
        id_field="neutral_id",
        many=True,
        include_resource_linkage=True,
        type_="categorisations",
        schema="CategorisationSchema",
    )

    class Meta(Schema.Meta):
        type_ = "categories"
        self_view = "category_terms_detail"
        self_view_kwargs = {"category_term_id": "<id>"}
        self_view_many = "category_terms_list"


class ParentCategoryTermSchema(CategoryTermSchema):
    class Meta(Schema.Meta):
        type_ = "categories"
        self_view = "category_terms_detail"
        self_view_kwargs = {"category_term_id": "<id>"}
        self_view_many = "category_terms_list"


class CategorisationSchema(Schema):
    id = fields.String(attribute="neutral_id", dump_only=True, required=True)

    project = Relationship(
        self_view="categorisations_relationship_projects",
        self_view_kwargs={"categorisation_id": "<neutral_id>"},
        related_view="categorisations_projects",
        related_view_kwargs={"categorisation_id": "<neutral_id>"},
        id_field="project.neutral_id",
        many=False,
        include_resource_linkage=True,
        type_="projects",
        schema="ProjectSchema",
    )

    category = Relationship(
        attribute="category_term",
        self_view="categorisations_relationship_category_terms",
        self_view_kwargs={"categorisation_id": "<neutral_id>"},
        related_view="categorisations_category_terms",
        related_view_kwargs={"categorisation_id": "<neutral_id>"},
        id_field="categorisation.neutral_id",
        many=False,
        include_resource_linkage=True,
        type_="categories",
        schema="CategoryTermSchema",
    )

    class Meta(Schema.Meta):
        type_ = "categorisations"
        self_view = "categorisations_detail"
        self_view_kwargs = {"categorisation_id": "<id>"}
        self_view_many = "categorisations_list"
