import random
import pytest
from faker import Faker
# noinspection PyPackageRequirements
from psycopg2.extras import DateRange
from arctic_office_projects_api.faker.providers.grant import GrantType
from arctic_office_projects_api.faker.providers.project import Provider  # Adjust the import based on your module structure

@pytest.fixture
def provider():
    fake = Faker()
    return Provider(fake)  # Pass the Faker generator to the Provider

def test_project_type(provider):
    grant_types = [provider.project_type() for _ in range(1000)]
    assert grant_types.count(GrantType.UKRI_STANDARD_GRANT) >= 200
    assert grant_types.count(GrantType.UKRI_LARGE_GRANT) >= 30
    assert grant_types.count(GrantType.EU_STANDARD_GRANT) >= 100
    assert grant_types.count(GrantType.OTHER) >= 200

def test_title(provider):
    title = provider.title()
    assert isinstance(title, str)
    assert 4 <= len(title.split()) <= 200

def test_has_acronym(provider):

    random.seed(1234)
    provider.faker.seed_instance(1234)

    acronym = provider.acronym()

    assert isinstance(acronym, str)
    assert acronym == 'STAR'

def test_acronym(provider):
    acronym = provider.acronym()
    assert isinstance(acronym, str)
    assert acronym.isupper()

def test_abstract(provider):
    abstract = provider.abstract()
    assert isinstance(abstract, str)

def test_has_website(provider):
    ukri_standard_true_count = sum(
        provider.has_website(GrantType.UKRI_STANDARD_GRANT) for _ in range(100)
    )
    assert 5 <= ukri_standard_true_count <= 70

    ukri_large_true_count = sum(
        provider.has_website(GrantType.UKRI_LARGE_GRANT) for _ in range(100)
    )
    assert 40 <= ukri_large_true_count <= 100

    eu_standard_true_count = sum(
        provider.has_website(GrantType.EU_STANDARD_GRANT) for _ in range(100)
    )
    assert eu_standard_true_count <= 100

    other_true_count = sum(
        provider.has_website(GrantType.OTHER) for _ in range(100)
    )
    assert 30 <= other_true_count <= 85

def test_has_publications(provider):
    has_publications = provider.has_publications()
    assert isinstance(has_publications, bool)

def test_publication(provider):
    doi = provider.publication()
    assert doi.startswith("https://doi.org/10.5555/")
    assert len(doi.split('/')[-1]) == 8  # Should have 8 digits

def test_publications_list(provider):
    publications = provider.publications_list()
    assert isinstance(publications, list)
    assert all(doi.startswith("https://doi.org/10.5555/") for doi in publications)

def test_project_duration(provider):
    grant_type = GrantType.UKRI_STANDARD_GRANT
    duration = provider.project_duration(grant_type)
    
    # Ensure it's an instance of DateRange
    assert isinstance(duration, DateRange)
    
    # Check if lower and upper bounds are not None
    assert duration.lower is not None  # Check start date
    assert duration.upper is not None  # Check end date

def test_has_existing_principle_investigator(provider):
    has_existing_pi = provider.has_existing_principle_investigator()
    assert isinstance(has_existing_pi, bool)

def test_has_existing_principle_investigator_organisation(provider):
    has_existing_org = provider.has_existing_principle_investigator_organisation()
    assert isinstance(has_existing_org, bool)

def test_has_co_investigators(provider):
    has_co_i = provider.has_co_investigators()
    assert isinstance(has_co_i, bool)

def test_co_investigator_count(provider):
    count = provider.co_investigator_count()
    assert isinstance(count, int)
    assert 1 <= count <= 25

def test_has_existing_co_investigator(provider):
    has_existing_co_i = provider.has_existing_co_investigator()
    assert isinstance(has_existing_co_i, bool)

def test_has_existing_co_investigator_organisation(provider):
    has_existing_org = provider.has_existing_co_investigator_organisation()
    assert isinstance(has_existing_org, bool)

def test_has_science_categories(provider):
    ukri_standard_true_count = sum(
        provider.has_science_categories(GrantType.UKRI_STANDARD_GRANT) for _ in range(100)
    )
    assert ukri_standard_true_count <= 100 

    ukri_large_true_count = sum(
        provider.has_science_categories(GrantType.UKRI_LARGE_GRANT) for _ in range(100)
    )
    assert ukri_large_true_count <= 100

    eu_standard_true_count = sum(
        provider.has_science_categories(GrantType.EU_STANDARD_GRANT) for _ in range(100)
    )
    assert eu_standard_true_count <= 100

    other_true_count = sum(
        provider.has_science_categories(GrantType.OTHER) for _ in range(100)
    )
    assert 30 <= other_true_count <= 85  

def test_science_categories_count(provider):
    count = provider.science_categories_count()
    assert isinstance(count, int)
    assert 1 <= count <= 6

