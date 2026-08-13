from enum import Enum
from arctic_office_projects_api.utils import (
    conditional_decorator,
    generate_neutral_id,
    generate_countries_enum
)


# Test for conditional_decorator
def test_conditional_decorator():
    # Test with condition True
    @conditional_decorator(lambda f: f, True)
    def test_function():
        return "unchanged"

    assert test_function() == "unchanged"

    # Test with condition False
    @conditional_decorator(lambda f: lambda: "decorated", False)
    def test_function_decorated():
        return "unchanged"

    assert test_function_decorated() == "decorated"


# Test for generate_neutral_id
def test_generate_neutral_id():
    # Call the function
    neutral_id = generate_neutral_id()

    # Assert that it is a string and matches ULID format (length 26)
    assert isinstance(neutral_id, str)
    assert len(neutral_id) == 26  # Length of a ULID


def test_generate_countries_enum():
    countries_enum = generate_countries_enum(name="TestCountries")

    # Ensure countries_enum is indeed of type Enum
    assert isinstance(countries_enum, type) and issubclass(
        countries_enum, Enum
    ), "countries_enum is not a valid Enum class"

    # Debug: print out the values in the generated enum
    print("Generated Countries Enum:")
    for country in countries_enum:
        print(f"{country.name}: {country.value}")

    # Verify that certain expected countries are present
    assert hasattr(countries_enum, "USA"), "Enum does not have USA"
    assert countries_enum.USA.value["name"] == "United States of America"
    assert countries_enum.USA.value["iso_3166_alpha3-code"] == "USA"

    # Optionally check for a few more countries to ensure coverage
    assert hasattr(countries_enum, "CAN"), "Enum does not have CAN"
    assert countries_enum.CAN.value["name"] == "Canada"
    assert countries_enum.CAN.value["iso_3166_alpha3-code"] == "CAN"

    assert hasattr(countries_enum, "GBR"), "Enum does not have GBR"
    assert (
        countries_enum.GBR.value["name"] == "United Kingdom of Great Britain and Northern Ireland"
    )
    assert countries_enum.GBR.value["iso_3166_alpha3-code"] == "GBR"
