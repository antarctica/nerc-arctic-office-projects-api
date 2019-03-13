# noinspection PyPackageRequirements
from marshmallow import MarshalResult, post_dump
from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema
from flask_sqlalchemy import Pagination
from typing import Union


class AppSchema(Schema):
    """
    Custom base Marshmallow schema class, based on marshmallow_jsonapi default 'flask' class

    All schemas in this application should inherit from this class.

    This class acts as a container for custom functionality and defaults related to returning JSON API formatted
    responses.
    """

    def __init__(self, *args, **kwargs):
        """
        Overloaded implementation of the marshmallow_jsonapi default 'schema' class

        Differences include:
        - pagination support implemented as a schema option

        """
        self.paginate = False
        self.current_page = None
        self.first_page = 1
        self.last_page = None
        self.next_page = None
        self.previous_page = None

        if 'paginate' in kwargs:
            self.paginate = kwargs['paginate']
            del kwargs['paginate']

        super().__init__(*args, **kwargs)

    def get_top_level_links(self, data: dict, many: bool) -> dict:
        """
        Overloaded implementation of the 'get_top_level_links' method in the marshmallow_jsonapi default 'schema' class

        Differences include:
        - pagination links included where multiple resources and pagination is used

        :type data: dict
        :param data: resource or resources to return
        :type many: bool
        :param many: whether a single or multiple resources are being returned

        :rtype dict
        :return: top-level links
        """
        links = {
            'self': None
        }

        if many:
            if self.opts.self_url_many:
                links['self'] = self.generate_url(self.opts.self_url_many)

                if self.paginate:
                    links['self'] = self.generate_url(self.opts.self_url_many, page=self.current_page)
        else:
            if self.opts.self_url:
                links['self'] = data.get('links', {}).get('self', None)

        if self.paginate:
            links['prev'] = None
            links['next'] = None
            links['first'] = self.generate_url(self.opts.self_url_many, page=self.first_page)
            links['last'] = self.generate_url(self.opts.self_url_many, page=self.last_page)
            if self.previous_page is not None:
                links['prev'] = self.generate_url(self.opts.self_url_many, page=self.previous_page)
            if self.next_page is not None:
                links['next'] = self.generate_url(self.opts.self_url_many, page=self.next_page)

        return links

    def generate_url(self, view_name: str, **kwargs) -> str:
        """
        Overloaded implementation of the 'generate_url' method in the marshmallow_jsonapi default 'flask' class

        Differences include:
        - '_external' parameter past to flask url_for method to generate absolute rather than relative URLs

        :type view_name: str
        :param view_name: name of flask view/route

        :param kwargs: arguments and other flask.url_for options

        :rtype str
        :return: generated URL
        """
        return super().generate_url(view_name, **kwargs, _external=True)

    def dump(
        self,
        obj: Union[list, Pagination],
        many: bool = None,
        update_fields: bool = True,
        **kwargs
    ) -> MarshalResult:
        """
        Overloaded implementation of the 'dump' method in the marshmallow default 'schema' class

        Differences include:
        - pagination support, FlaskSQLAlchemy pagination objects can be given, in addition to one or more resources

        :type obj: Union[list, Pagination]
        :param obj: input data
        :type many: bool
        :param many: whether a single or multiple resources are being returned
        :type update_fields: bool
        :param update_fields: Whether to update the schema's field classes. Typically set to `True`, but may be `False`
            when serializing a homogeneous collection. This parameter is used by `fields.Nested` to avoid multiple
            updates.

        :rtype: `MarshalResult`, a `collections.namedtuple`
        :return: A tuple of the form (``data``, ``errors``)
        """
        if self.paginate:
            if not isinstance(obj, Pagination):
                raise ValueError("Pagination dumping requires a FlaskSQLAlchemy pagination object.")

            self.current_page = obj.page
            self.last_page = obj.pages
            if obj.has_next:
                self.next_page = obj.next_num
            if obj.has_prev:
                self.previous_page = obj.prev_num
            return super().dump(obj.items, many=many, update_fields=update_fields, **kwargs)

        return super().dump(obj, many=many, update_fields=update_fields, **kwargs)

    class Meta:
        """
        Custom base Marshmallow schema metadata class

        All schemas in this application should inherit from this class for its metadata.

        This class acts as a container for custom functionality and defaults related to returning JSON API formatted
        responses.
        """

        @staticmethod
        def _inflection(field: str) -> str:
            """
            Converts underscores in field names to hyphens as preferred by JsonAPI specification

            :type field: str
            :param field: name of field to be converted
            :rtype str
            :return: converted field name
            """
            return field.replace('_', '-')

        strict = True
        inflect = _inflection


class ProjectSchema(AppSchema):
    """
    Represents information about a research project
    """
    id = fields.Str(attribute="neutral_id", dump_only=True, required=True)
    title = fields.Str(dump_only=True, required=True)

    people = fields.Relationship(
        self_url='main.projects_people_relationship',
        self_url_kwargs={'project_id': '<id>'},
        related_url='/projects/{project_id}/people',
        related_url_kwargs={'project_id': '<id>'},
        id_field='neutral_id',
        many=True,
        include_resource_linkage=True,
        type_='participants',
    )

    @post_dump
    def transform(self, data: dict) -> dict:
        return data

    class Meta(AppSchema.Meta):
        type_ = 'project'
        self_view = 'main.projects_detail'
        self_view_kwargs = {'project_id': '<id>'}
        self_view_many = 'main.projects_list'


class PersonSchema(AppSchema):
    """
    Represents information about an individual
    """
    id = fields.Str(attribute="neutral_id", dump_only=True, required=True)
    first_name = fields.Str(dump_only=True, required=True)
    last_name = fields.Str(dump_only=True, required=True)

    class Meta(AppSchema.Meta):
        type_ = 'project'
        self_view = 'main.people_detail'
        self_view_kwargs = {'person_id': '<id>'}
        self_view_many = 'main.people_list'
