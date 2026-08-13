import pytest
from faker import Faker
from arctic_office_projects_api.faker.providers.person import Provider


# Setup a Faker instance and add the custom provider.
@pytest.fixture
def provider():
    fake = Faker()
    provider = Provider(fake)
    return provider


def test_male_or_female_output(provider):
    """
    Test that the method returns either 'male' or 'female'.
    """
    result = provider.male_or_female()
    assert result in ["male", "female"], f"Unexpected result: {result}"


def test_male_or_female_randomness(provider):
    """
    Test that calling the method multiple times returns both 'male' and 'female' at least once.
    """
    # results = {provider.male_or_female() for _ in range(100)}
    # Assert that bo
