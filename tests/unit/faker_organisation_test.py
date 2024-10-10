import pytest
import re
from unittest.mock import patch
from faker import Faker
from arctic_office_projects_api.faker.providers.organisation import get_string, Provider

# ------------- Tests for get_string function -------------


def test_get_string_length():
    result = get_string(5, 3)
    assert len(result) == 8  # 5 letters + 3 digits = 8 characters in total


def test_get_string_contains_letters_and_digits():
    result = get_string(4, 4)
    assert len([c for c in result if c.isalpha()]) == 4  # Check the number of letters
    assert len([c for c in result if c.isdigit()]) == 4  # Check the number of digits


def test_get_string_shuffled():
    with patch("random.shuffle") as mock_shuffle:
        get_string(3, 3)
        assert mock_shuffle.called  # Ensure shuffle was called


# ------------- Tests for Provider class -------------


@pytest.fixture
def provider():
    fake = Faker()
    fake.add_provider(Provider)
    return fake


def test_grid_id_format(provider):
    grid_id = provider.grid_id()
    assert re.match(r"^XE-EXAMPLE-grid\.5\d{3,5}\.\d{1,2}$", grid_id)  # Check format


def test_grid_id_value_ranges(provider):
    grid_id = provider.grid_id()
    # Extract the numeric identifier from the Grid ID
    identifier = int(re.search(r"grid\.5(\d+)\.", grid_id).group(1))
    # Ensure the identifier is in the correct range (100-999, 1000-9999, or 10000-99999)
    assert 100 <= identifier <= 99999


def test_ror_id_format(provider):
    ror_id = provider.ror_id()

    # Ensure that the total length is 9 (4 letters + 5 digits)
    assert len(ror_id) == 9

    # Ensure there are exactly 4 letters and 5 digits
    letters = [c for c in ror_id if c.isalpha()]
    digits = [c for c in ror_id if c.isdigit()]

    assert len(letters) == 4  # Check for 4 letters
    assert len(digits) == 5  # Check for 5 digits


def test_ror_id_length(provider):
    ror_id = provider.ror_id()
    assert len(ror_id) == 9  # 4 letters + 5 digits = 9 characters in total
