from datetime import datetime
from enum import Enum
from typing import Union, Optional

from flask_sqlalchemy.model import Model
from flask_sqlalchemy.pagination import Pagination

# noinspection PyPackageRequirements
from marshmallow import post_dump

# noinspection PyPackageRequirements
from marshmallow.fields import Field
from marshmallow_jsonapi.flask import (
    Schema as _Schema,
    Relationship as _Relationship
)

# noinspection PyPackageRequirements
from psycopg2.extras import DateRange


class Schema(_Schema):
    """
    Custom base Marshmallow schema class, based on marshmallow_jsonapi
    default 'flask' class

    All schemas in this application should inherit from this class.

    Implements or related to:
    * https://github.com/marshmallow-code/marshmallow-jsonapi/issues/57
        * https://github.com/marshmallow-code/marshmallow-jsonapi/pull/64
    * https://github.com/marshmallow-code/marshmallow-jsonapi/issues/195
    """

    def __init__(self, *args, **kwargs):
        """
        Overloaded implementation of the marshmallow_jsonapi
        default 'schema' class

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

        if "paginate" in kwargs:
            self.paginate = kwargs["paginate"]
            del kwargs["paginate"]

        if "resource_linkage" in kwargs:
            self.resource_linkage = kwargs["resource_linkage"]
            del kwargs["resource_linkage"]
        if "related_resource" in kwargs:
            self.related_resource = kwargs["related_resource"]
            kwargs["include_data"] = (self.related_resource,)
            del kwargs["related_resource"]
        if "many_related" in kwargs:
            self.many_related = kwargs["many_related"]
            del kwargs["many_related"]

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
        links = {"self": None}

        if many:
            if self.opts.self_url_many:
                links["self"] = self.generate_url(self.opts.self_url_many)

                if self.paginate:
                    links["self"] = self.generate_url(
                        self.opts.self_url_many, page=self.current_page
                    )
        else:
            if self.opts.self_url:
                links["self"] = data.get("links", {}).get("self", None)

        if self.paginate:
            links["prev"] = None
            links["next"] = None
            links["first"] = self.generate_url(
                self.opts.self_url_many, page=self.first_page
            )
            links["last"] = self.generate_url(
                self.opts.self_url_many, page=self.last_page
            )
            if self.previous_page is not None:
                links["prev"] = self.generate_url(  # pragma: no cover
                    self.opts.self_url_many, page=self.previous_page
                )
            if self.next_page is not None:
                links["next"] = self.generate_url(
                    self.opts.self_url_many, page=self.next_page
                )

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
        **kwargs,
    ) -> dict:
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

        :rtype: dict
        :return: A dict of serialized data
        """
        if self.paginate:
            if not isinstance(obj, Pagination):
                raise ValueError(  # pragma: no cover
                    "Pagination dumping requires a FlaskSQLAlchemy pagination object."
                )

            self.current_page = obj.page
            self.last_page = obj.pages
            if obj.has_next:
                self.next_page = obj.next_num
            if obj.has_prev:
                self.previous_page = obj.prev_num  # pragma: no cover
            return super().dump(obj.items, many=many)

        return super().dump(obj, many=many)

    @post_dump(pass_many=True)
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
            if many:  # pragma: no cover
                raise RuntimeError(  # pragma: no cover
                    "A resource linkage can't be returned for multiple resources"
                )

            if (
                self.resource_linkage in response["data"]["relationships"]
            ):  # pragma: no cover
                return response["data"]["relationships"][
                    self.resource_linkage
                ]  # pragma: no cover

            raise KeyError(
                f"No relationship found for '{ self.resource_linkage }'"
            )  # pragma: no cover

        if self.related_resource is not None:
            # Inflect related resource so it can be found in pre-generated output
            related_resource = self.related_resource.replace(
                "_", "-"
            )  # pragma: no cover

            if many:  # pragma: no cover
                raise RuntimeError(  # pragma: no cover
                    "A related resource response can't be returned for multiple resources"
                )

            if (
                related_resource in response["data"]["relationships"]
            ):  # pragma: no cover
                if (
                    "links" in response["data"]["relationships"][related_resource]
                ):  # pragma: no cover
                    if (  # pragma: no cover
                        "related"
                        in response["data"]["relationships"][related_resource]["links"]
                    ):
                        _response = {  # pragma: no cover
                            "data": [],
                            "links": {
                                "self": response["data"]["relationships"][
                                    related_resource
                                ]["links"]["related"]
                            },
                        }
                        if not self.many_related:  # pragma: no cover
                            _response["data"] = None  # pragma: no cover

                        if "included" in response:  # pragma: no cover
                            _response["data"] = response["included"]  # pragma: no cover
                            if not self.many_related:  # pragma: no cover
                                _response["data"] = _response["data"][
                                    0
                                ]  # pragma: no cover

                        return _response  # pragma: no cover
                    raise KeyError(  # pragma: no cover
                        f"No related resource link found for '{related_resource}' relationship"
                    )
                raise KeyError(
                    f"No links found for '{related_resource}' relationship"
                )  # pragma: no cover
            raise KeyError(
                f"No relationship found for '{related_resource}'"
            )  # pragma: no cover

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
            return field.replace("_", "-")

        strict = True
        inflect = _inflection
        json_schema = None


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
        view_kwargs["_external"] = True
        return super().get_url(obj, view_name, view_kwargs)


class DateRangeField(Field):
    """
    Custom Marshmallow field for the PostgreSQL DateRange class
    """

    def _serialize(self, value: DateRange, attr: str, obj, **kwargs) -> dict:
        """
        When serialising, the DateRange is converted into a dict containing a ISO 8601 date interval, covering the date
        range, and two date instants, indicating the beginning and end of the date range.

        Where either side of a date range is unbound, '..' will be substituted and the relevant date instant set to
        None/null. E.g. An unbound end will use '2012-10-30/..' and an unbound start will use '../2040-10-12'.

        :type value: DateRange
        :param value: a DateRange instance
        :type attr: str
        :param attr: name of the field within the schema being dumped
        :param obj: the object 'value' was taken from
        :type kwargs: dict
        :param kwargs: field-specific keyword arguments

        :rtype: dict
        :return: ISO 8601 date interval and date instants for the beginning and end of a date range
        """
        instant_start = None
        instant_end = None
        interval_start = ".."
        interval_end = ".."

        if value.lower is not None:
            instant_start = value.lower.isoformat()
            interval_start = instant_start
        if value.upper is not None:
            instant_end = value.upper.isoformat()
            interval_end = instant_end

        return {
            "interval": f"{ interval_start }/{ interval_end }",
            "start-instant": instant_start,
            "end-instant": instant_end,
        }

    # noinspection PyMethodOverriding
    def deserialize(self, value: dict, attr: str, data: dict) -> DateRange:
        """
        When serialising it's expected that a ParticipantRole enumerator item is specified by an 'interval' value key,
        which is a ISO 8601 date interval consisting of two ISO 8601 dates that cover the date range.

        :type value: dict
        :param value: dictionary containing at least an 'interval' field which corresponds to a ISO 8601 date interval
        :param attr: name of the field within the schema being loaded
        :param data: the object 'value' was taken from, in this case the data to be loaded

        :rtype: DateRange
        :return: a DateRange instance
        """
        if "interval" not in value.keys():
            raise KeyError(f"No 'interval' property in { attr } to cover date range")

        interval = value["interval"].split("/")
        if len(interval) != 2:
            raise ValueError(
                f"Interval '{ value['interval'] }' is not in the form [start date]/[end date]"
            )

        try:
            interval = DateRange(
                datetime.strptime(interval[0], "%Y-%m-%d"),
                datetime.strptime(interval[1], "%Y-%m-%d"),
            )
            return interval
        except ValueError:  # pragma: no cover
            raise ValueError(  # pragma: no cover
                f"Invalid '{ value['interval'] }' is not in the form [YYYY-MM-DD]/[YYYY-MM-DD]"
            )


class EnumField(Field):
    """
    Base custom Marshmallow field for values from an enumerator class

    E.g.
        class Foo(Enum):
            Foo = 'bar'
    """

    def _serialize(self, value: Enum, attr: str, obj: Model, **kwargs):
        """
        When serialising, the value of the enumerator item corresponding to the 'value' parameter is returned.

        :type value: Enum
        :param value: an item within the enumerator
        :type attr: str
        :param attr: name of the field within the schema being dumped
        :type obj: Model
        :param obj: the object 'value' was taken from, in this case an SQLAlchemy model instance
        :type kwargs: dict
        :param kwargs: field-specific keyword arguments

        :return: the enumerator item's value
        """
        if value is None:
            return None

        if isinstance(value.value, dict):
            return self._inflection(value.value)

        return value.value

    def _inflection(self, dictionary: dict) -> dict:
        """
        Recursively replaces dictionary keys containing a '_' with '-'

        E.g. "{'foo_bar: {'foo_bar: 'baz'}}" would become "{'foo-bar: {'foo-bar: 'baz'}}"

        :type dictionary: dict
        :param dictionary: dictionary to inflect

        :rtype: dict
        :return: inflected dictionary
        """
        converted_dict = {}
        for k, v in dictionary.items():
            if isinstance(v, dict):
                v = self._inflection(v)  # pragma: no cover
            converted_dict[k.replace("_", "-")] = v
        return converted_dict


class EnumStrField(EnumField):
    """
    Custom Marshmallow field for string values from an enumerator class

    E.g.
        class Foo(Enum):
            Foo = 'bar'
    """

    def _serialize(self, value: Enum, attr: str, obj: Model, **kwargs) -> str:
        """
        When serialising, the value of the enumerator item corresponding to the 'value' parameter is returned.

        :type value: Enum
        :param value: an item within the enumerator
        :type attr: str
        :param attr: name of the field within the schema being dumped
        :type obj: Model
        :param obj: the object 'value' was taken from, in this case an SQLAlchemy model instance
        :type kwargs: dict
        :param kwargs: field-specific keyword arguments

        :rtype: str
        :return: the enumerator item's value
        """
        # noinspection PyTypeChecker
        return super()._serialize(value, attr, obj)


class EnumDictField(EnumField):
    """
    Custom Marshmallow field for dictionary values from an enumerator class

    E.g.
        class Foo(Enum):
            Foo = {'bar': 'baz'}
    """

    def _serialize(self, value: Enum, attr: str, obj: Model, **kwargs) -> dict:
        """
        When serialising, the value of the enumerator item corresponding to the 'value' parameter is returned.

        :type value: Enum
        :param value: an item within the enumerator
        :type attr: str
        :param attr: name of the field within the schema being dumped
        :type obj: Model
        :param obj: the object 'value' was taken from, in this case an SQLAlchemy model instance
        :type kwargs: dict
        :param kwargs: field-specific keyword arguments


        :rtype: dict
        :return: the enumerator item's value
        """
        return super()._serialize(value, attr, obj)


class CurrencyField(Field):
    """
    Custom Marshmallow field for a currency value

    This field requires a metadata argument with a field in the schema object containing a currency value from an
    enumeration of currency information.

    Field use example:

        class FooSchema(Schema):
            cost = CurrencyField(currency='cost_currency')

    Where 'cost_currency' is a property containing an item form an enumeration, which is structured as a dictionary:

        class GrantCurrency(Enum):
            GBP = {
                'iso_4217_code': 'GBP',
                'major_symbol': '£'
            }
    """

    def _serialize(
        self, value: float, attr: str, obj: Model, **kwargs
    ) -> Optional[dict]:
        """
        When serialising, a numeric value is combined with currency unit defined by a metadata argument

        See the class definition for how to specify the currency metadata argument.

        :type value: float
        :param value: numeric value which will be combined with a currency
        :type attr: str
        :param attr: name of the field within the schema being dumped
        :type obj: Model
        :param obj: the object containing the numeric value and currency unit, in this case a SQLAlchemy model
        :type kwargs: dict
        :param kwargs: field-specific keyword arguments

        :rtype: dict
        :return: a numeric value is combined with currency unit
        """
        if value is None:
            return None  # pragma: no cover

        if "currency" not in self.metadata:
            raise KeyError(
                "Missing currency unit in field metadata"
            )  # pragma: no cover
        currency = getattr(obj, self.metadata["currency"])

        if currency is None:
            raise ValueError("The currency unit cannot be None")  # pragma: no cover
        if not isinstance(currency, Enum):
            raise TypeError(  # pragma: no cover
                "The currency unit value is expected to be from an enumeration"
            )
        if type(currency.value) is not dict:
            raise TypeError(  # pragma: no cover
                "The currency unit enumeration value is expected to be a dictionary"
            )

        return {
            "value": value,
            "currency": {
                "iso-4217-code": currency.value["iso_4217_code"],
                "major-symbol": currency.value["major_symbol"],
            },
        }
