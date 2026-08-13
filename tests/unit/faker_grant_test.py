from psycopg2.extras import DateRange
from datetime import date, timedelta
from faker import Faker
from arctic_office_projects_api.faker.providers.grant import (
    Provider,
    GrantType,
    GrantCurrency,
    GrantStatus,
    UKRICouncil,
)

# Initialize Faker and Provider
faker = Faker()
provider = Provider(faker)


# Tests for grant_currency method
def test_grant_currency_ukri_standard_grant():
    assert provider.grant_currency(GrantType.UKRI_STANDARD_GRANT) == GrantCurrency.GBP


def test_grant_currency_eu_standard_grant():
    assert provider.grant_currency(GrantType.EU_STANDARD_GRANT) == GrantCurrency.EUR


def test_grant_currency_other_grant():
    currency = provider.grant_currency(GrantType.OTHER)
    assert currency in [
        GrantCurrency.GBP,
        GrantCurrency.EUR,
        GrantCurrency.NOK,
        GrantCurrency.CAD,
    ]


# Tests for grant_reference method
def test_grant_reference_ukri_standard_grant():
    reference = provider.grant_reference(
        GrantType.UKRI_STANDARD_GRANT, UKRICouncil.NERC
    )
    assert reference.startswith("NE/")


def test_grant_reference_eu_standard_grant():
    reference = provider.grant_reference(GrantType.EU_STANDARD_GRANT, None)
    assert len(reference) == 6


def test_grant_reference_other_grant():
    reference = provider.grant_reference(GrantType.OTHER, None)
    assert len(reference) <= 20


# Tests for total_funds method
def test_total_funds_ukri_standard_grant():
    total = provider.total_funds(GrantType.UKRI_STANDARD_GRANT)
    assert 1000 <= total <= 80000


def test_total_funds_ukri_large_grant():
    total = provider.total_funds(GrantType.UKRI_LARGE_GRANT)
    assert 3000000 <= total <= 3700000


def test_total_funds_eu_standard_grant():
    total = provider.total_funds(GrantType.EU_STANDARD_GRANT)
    assert 2000000 <= total <= 10000000


def test_total_funds_other_grant():
    total = provider.total_funds(GrantType.OTHER)
    assert 100 <= total <= 300000


# Tests for grant_status method
def test_grant_status_active_with_no_end_date():
    duration = DateRange(date.today(), None)
    assert provider.grant_status(duration) == GrantStatus.Active


def test_grant_status_active_with_future_end_date():
    duration = DateRange(
        date.today() - timedelta(days=10), date.today() + timedelta(days=10)
    )
    assert provider.grant_status(duration) == GrantStatus.Active


def test_grant_status_closed():
    duration = DateRange(
        date.today() - timedelta(days=365), date.today() - timedelta(days=10)
    )
    assert provider.grant_status(duration) == GrantStatus.Closed


# Tests for grant_funder method
def test_grant_funder_ukri_standard_grant():
    funder = provider.grant_funder(GrantType.UKRI_STANDARD_GRANT)
    assert funder in [council.name for council in UKRICouncil]


def test_grant_funder_eu_standard_grant():
    assert provider.grant_funder(GrantType.EU_STANDARD_GRANT) == "EU"


def test_grant_funder_other_grant():
    funder = provider.grant_funder(GrantType.OTHER)
    assert funder in [True, None]


# Tests for grant_website method
def test_grant_website_ukri_grant():
    reference = "ST/F006446/1"
    website = provider.grant_website(GrantType.UKRI_STANDARD_GRANT, reference)
    assert website == "https://gtr.ukri.org/projects?ref=ST%2FF006446%2F1"


def test_grant_website_eu_grant():
    reference = "217700"
    website = provider.grant_website(GrantType.EU_STANDARD_GRANT, reference)
    assert website == f"https://cordis.europa.eu/project/rcn/{reference}"
