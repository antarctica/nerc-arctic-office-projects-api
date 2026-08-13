import pytest
from unittest.mock import patch, Mock
from datetime import datetime
from marshmallow import fields
from arctic_office_projects_api.models import Enum
from arctic_office_projects_api.schemas_extension import (
    Schema,
    Relationship,
    DateRangeField,
    EnumField,
    CurrencyField,
    EnumStrField,
)


# Test data and enums
class SampleEnum(Enum):
    OPTION1 = "option1"
    OPTION2 = "option2"


class ExampleSchema(Schema):
    field1 = EnumField()
    field2 = DateRangeField()
    currency = CurrencyField(metadata={"currency": "currency_type"})


class MyEnum(Enum):
    VALUE1 = "value1"
    VALUE2 = "value2"


class MySchema(Schema):
    class Meta(Schema.Meta):
        type_ = "test"

    id = fields.String(dump_only=True, required=True)
    field1 = EnumStrField(metadata={"enum": MyEnum}, dump_only=True, required=True)
    cost_currency = fields.String(required=True)  # Include the currency field
    cost = CurrencyField(metadata={"currency": "currency_type"}, required=True)  # Initialize CurrencyField


@pytest.fixture
def sample_schema():
    class ExampleSchema(Schema):
        class Meta(Schema.Meta):
            type_ = "test"

        id = fields.String(dump_only=True, required=True)
        name = fields.String(dump_only=True)

    return ExampleSchema()


def test_schema_initialization(sample_schema):
    assert sample_schema.paginate is False
    assert sample_schema.resource_linkage is None


def test_enum_field_serialization():
    schema = MySchema()
    data = {"id": "123", "field1": MyEnum.VALUE1}
    result = schema.dump(data)

    assert result["data"]["attributes"]["field1"] == "value1"


def test_enum_field_serialization_none(sample_schema):
    schema = MySchema()
    data = {"id": "123", "field1": None}
    result = schema.dump(data)
    assert result["data"]["attributes"]["field1"] is None


def test_relationship_get_url():
    relationship = Relationship()
    obj = Mock()
    view_name = "test_view"
    view_kwargs = {}

    with patch("flask.url_for", return_value="http://test.com/test_view"):
        url = relationship.get_url(obj, view_name, view_kwargs)
        assert url == "http://test.com/test_view"


def test_date_range_field_deserialization():
    field = DateRangeField()
    data = {"interval": "2022-01-01/2022-12-31"}

    result = field.deserialize(data, "field2", {})
    assert result.lower == datetime(2022, 1, 1)
    assert result.upper == datetime(2022, 12, 31)


def test_date_range_field_deserialization_invalid_interval():
    field = DateRangeField()
    data = {"interval": "invalid-interval"}

    with pytest.raises(ValueError):
        field.deserialize(data, "field2", {})


def test_date_range_field_deserialization_missing_interval():
    field = DateRangeField()
    data = {}

    with pytest.raises(KeyError):
        field.deserialize(data, "field2", {})


# Run the tests
if __name__ == "__main__":
    pytest.main()
