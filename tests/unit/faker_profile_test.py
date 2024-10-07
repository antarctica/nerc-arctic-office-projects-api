import pytest
from faker import Faker
from faker.providers import BaseProvider

# Import the Provider class
from arctic_office_projects_api.faker.providers.profile import Provider

@pytest.fixture
def fake():
    """Fixture to set up a Faker generator with the custom Provider."""
    fake = Faker()
    fake.add_provider(Provider)
    return fake

def test_has_orcid_id(fake):
    """Test the has_orcid_id function returns a boolean and respects the weighted distribution."""
    result = fake.has_orcid_id()
    assert isinstance(result, bool), "has_orcid_id should return a boolean"

    # Test the 80/20 distribution of True/False over multiple runs
    true_count = sum(fake.has_orcid_id() for _ in range(1000))
    assert 450 <= true_count <= 850, "Expected roughly ...% of results to be True"

def test_orcid_id(fake):
    """Test the orcid_id function returns a valid formatted ORCID URL."""
    orcid = fake.orcid_id()
    assert orcid.startswith("https://fake.orcid.org/0000-"), "orcid_id should start with 'https://fake.orcid.org/0000-'"
    parts = orcid.split("-")
    assert len(parts) == 4, "ORCID ID should be in the format 'https://fake.orcid.org/0000-xxxx-xxxx-xxxx'"
    assert all(part.isdigit() for part in parts[1:]), "Each part of the ORCID ID should be numeric"

def test_has_avatar(fake):
    """Test the has_avatar function returns a boolean and respects the weighted distribution."""
    result = fake.has_avatar()
    assert isinstance(result, bool), "has_avatar should return a boolean"

    # Test the 7/93 distribution of True/False over multiple runs
    true_count = sum(fake.has_avatar() for _ in range(1000))
    assert 50 <= true_count <= 600, "Expected roughly ...% of results to be True"

def test_avatar(fake):
    """Test the avatar function returns a valid avatar URL."""
    avatar = fake.avatar()
    assert avatar.startswith("https://randomuser.me/api/portraits/"), "Avatar URL should start with 'https://randomuser.me/api/portraits/'"
    
    # Check if it's either male or female
    assert any(gender in avatar for gender in ['men', 'women']), "Avatar URL should contain 'men' or 'women'"
    
    # Ensure the numeric part is within range
    parts = avatar.split('/')
    number_part = parts[-1].replace('.jpg', '')
    assert number_part.isdigit() and 1 <= int(number_part) <= 99, "Avatar number should be between 1 and 99"

def test_avatar_male(fake):
    """Test the avatar_male function returns a valid male avatar URL."""
    avatar_male = fake.avatar_male()
    assert avatar_male.startswith("https://randomuser.me/api/portraits/men/"), "Avatar male URL should start with 'https://randomuser.me/api/portraits/men/'"
    
    # Ensure the numeric part is within range
    parts = avatar_male.split('/')
    number_part = parts[-1].replace('.jpg', '')
    assert number_part.isdigit() and 1 <= int(number_part) <= 99, "Male avatar number should be between 1 and 99"

def test_avatar_female(fake):
    """Test the avatar_female function returns a valid female avatar URL."""
    avatar_female = fake.avatar_female()
    assert avatar_female.startswith("https://randomuser.me/api/portraits/women/"), "Avatar female URL should start with 'https://randomuser.me/api/portraits/women/'"
    
    # Ensure the numeric part is within range
    parts = avatar_female.split('/')
    number_part = parts[-1].replace('.jpg', '')
    assert number_part.isdigit() and 1 <= int(number_part) <= 99, "Female avatar number should be between 1 and 99"
