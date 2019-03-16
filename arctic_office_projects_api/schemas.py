# noinspection PyPackageRequirements
import marshmallow

# noinspection PyPackageRequirements
from marshmallow import MarshalResult
from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema as _Schema, Relationship as _Relationship
from flask_sqlalchemy import Pagination
from typing import Union


class Schema(_Schema):
    """
    Custom base Marshmallow schema class, based on marshmallow_jsonapi default 'flask' class

    All schemas in this application should inherit from this class.
    """

    def __init__(self, *args, **kwargs):
        """
        Overloaded implementation of the marshmallow_jsonapi default 'schema' class

        Differences include:
        - pagination support implemented as a schema option
        - resource linkage support, implemented as a schema option
        - related resource support, implemented as a schema option
        """
        self.paginate = False
        self.current_page = None
        self.first_page = 1
        self.last_page = None
        self.next_page = None
        self.previous_page = None

        self.resource_linkage = None
        self.related_resource = None
        self.many_related = False

        if 'paginate' in kwargs:
            self.paginate = kwargs['paginate']
            del kwargs['paginate']

        if 'resource_linkage' in kwargs:
            self.resource_linkage = kwargs['resource_linkage']
            del kwargs['resource_linkage']
        if 'related_resource' in kwargs:
            self.related_resource = kwargs['related_resource']
            kwargs['include_data'] = (self.related_resource,)
            del kwargs['related_resource']
        if 'many_related' in kwargs:
            self.many_related = kwargs['many_related']
            del kwargs['many_related']

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

    @marshmallow.post_dump(pass_many=True)
    def format_json_api_response(self, data: dict, many: bool) -> dict:
        """
        Overloaded implementation of the 'format_json_api_response' method in the marshmallow_jsonapi default schema
        class

        Differences include:
        - resource linkage support, modifies a standard schema response to return a JSON API resource linkage
        - related resource support, modifies a standard schema response to return the contents of a JSON API related
          resource link

        :type data: dict
        :param data: resource or resources to return
        :type many: bool
        :param many: whether a single or multiple resources are being returned

        :rtype dict
        :return: top-level response
        """
        response = super().format_json_api_response(data, many)

        if self.resource_linkage is not None:
            if many:
                raise RuntimeError('A resource linkage can\'t be returned for multiple resources')

            if self.resource_linkage in response['data']['relationships']:
                return response['data']['relationships'][self.resource_linkage]

            raise KeyError(f"No relationship found for '{ self.resource_linkage }'")

        if self.related_resource is not None:
            if many:
                raise RuntimeError('A related resource response can\'t be returned for multiple resources')

            if self.related_resource in response['data']['relationships']:
                if 'links' in response['data']['relationships'][self.related_resource]:
                    if 'related' in response['data']['relationships'][self.related_resource]['links']:
                        if 'included' in response:
                            response = {
                                'data': response['included'],
                                'links': {
                                    'self': response['data']['relationships'][self.related_resource]['links']['self']
                                }
                            }
                            if not self.many_related:
                                response['data'] = response['data'][0]

                            return response

                        raise KeyError(f"No related resources are defined for '{ self.related_resource }'")
                    raise KeyError(f"No related resource link found for '{ self.related_resource }' relationship")
                raise KeyError(f"No links found for '{self.related_resource}' relationship")
            raise KeyError(f"No relationship found for '{self.related_resource}'")

        return response

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


class Relationship(_Relationship):
    """
    Custom base marshmallow_jsonapi schema relationship class, based on the default 'flask' class

    All schema relationships in this application should inherit from this class.
    """

    def get_url(self, obj, view_name, view_kwargs):
        """
        Overloaded implementation of the 'get_url' method in the marshmallow_jsonapi default 'flask' class

        Differences include:
        - '_external' parameter past to flask url_for method to generate absolute rather than relative URLs

        :param obj: relationship object
        :type view_name: str
        :param view_name: name of flask view/route
        :param view_kwargs: arguments and other flask.url_for options

        :rtype str
        :return: generated URL
        """
        view_kwargs['_external'] = True
        return super().get_url(obj, view_name, view_kwargs)


class ProjectSchema(Schema):
    """
    Represents information about a research project
    """
    id = fields.Str(attribute="neutral_id", dump_only=True, required=True)
    title = fields.Str(dump_only=True, required=True)

    participants = Relationship(
        self_view='main.projects_relationship_participants',
        self_view_kwargs={'project_id': '<neutral_id>'},
        related_view='main.projects_participants',
        related_view_kwargs={'project_id': '<neutral_id>'},
        id_field='neutral_id',
        many=True,
        include_resource_linkage=True,
        type_='participants',
        schema='ParticipantSchema'
    )

    class Meta(Schema.Meta):
        type_ = 'projects'
        self_view = 'main.projects_detail'
        self_view_kwargs = {'project_id': '<id>'}
        self_view_many = 'main.projects_list'


class ParticipantSchema(Schema):
    id = fields.Str(attribute="neutral_id", dump_only=True, required=True)
    investigative_role = fields.Str(dump_only=True, required=True)

    project = Relationship(
        self_view='main.participants_relationship_projects',
        self_view_kwargs={'participant_id': '<neutral_id>'},
        related_view='main.participants_projects',
        related_view_kwargs={'participant_id': '<neutral_id>'},
        id_field='project.neutral_id',
        include_resource_linkage=True,
        type_='projects',
        schema='ProjectSchema'
    )

    person = Relationship(
        self_view='main.participants_relationship_people',
        self_view_kwargs={'participant_id': '<neutral_id>'},
        related_view='main.participants_people',
        related_view_kwargs={'participant_id': '<neutral_id>'},
        id_field='person.neutral_id',
        include_resource_linkage=True,
        type_='people',
        schema='PersonSchema'
    )

    class Meta(Schema.Meta):
        type_ = 'participants'
        self_view = 'main.participants_detail'
        self_view_kwargs = {'participant_id': '<id>'}
        self_view_many = 'main.participants_list'


class PersonSchema(Schema):
    id = fields.Str(attribute="neutral_id", dump_only=True, required=True)
    first_name = fields.Str(dump_only=True, required=True)
    last_name = fields.Str(dump_only=True, required=True)

    participation = Relationship(
        self_view='main.people_relationship_participants',
        self_view_kwargs={'person_id': '<neutral_id>'},
        related_view='main.people_participants',
        related_view_kwargs={'person_id': '<neutral_id>'},
        id_field='neutral_id',
        many=True,
        include_resource_linkage=True,
        type_='participants',
        schema='ParticipantSchema'
    )

    class Meta(Schema.Meta):
        type_ = 'people'
        self_view = 'main.people_detail'
        self_view_kwargs = {'person_id': '<id>'}
        self_view_many = 'main.people_list'
