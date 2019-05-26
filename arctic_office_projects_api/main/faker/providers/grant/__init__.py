from datetime import date
from enum import Enum

from faker import Faker
from faker.providers import BaseProvider
# noinspection PyPackageRequirements
from psycopg2.extras import DateRange

localized = False


class UKRICouncil(Enum):
    """
    Represents the research councils within UK Research and Innovation (UKRI)
    """
    AHRC = {
        'acronym': 'AHRC',
        'prefix': 'AH'
    }
    BBSRC = {
        'acronym': 'BBSRC',
        'prefix': 'BB'
    }
    EPSRC = {
        'acronym': 'EPSRC',
        'prefix': 'EP'
    }
    ESRC = {
        'acronym': 'ESRC',
        'prefix': 'ES'
    }
    MRC = {
        'acronym': 'MRC',
        'prefix': 'G'
    }
    NERC = {
        'acronym': 'NERC',
        'prefix': 'NE'
    }
    STFC = {
        'acronym': 'STFC',
        'prefix': 'ST'
    }


class GrantCurrency(Enum):
    """
    Represents the various currencies of a research grant
    """
    GBP = {
        'iso_4217_code': 'GBP',
        'major_symbol': '£'
    }
    EUR = {
        'iso_4217_code': 'EUR',
        'major_symbol': '€'
    }
    USD = {
        'iso_4217_code': 'USD',
        'major_symbol': '$'
    }


class GrantType(Enum):
    UKRI_STANDARD_GRANT = 'ukri-standard-grant'
    UKRI_LARGE_GRANT = 'ukri-large-grant'
    EU_STANDARD_GRANT = 'eu-standard-grant'
    OTHER = 'other-grant'


class GrantStatus(Enum):
    """
    Represents the various states of a research grant
    """
    Accepted = {
        'title': 'accepted'
    }
    Active = {
        'title': 'active'
    }
    Approved = {
        'title': 'approved'
    }
    Authorised = {
        'title': 'active'
    }
    Closed = {
        'title': 'closed'
    }


class Provider(BaseProvider):
    faker = Faker()

    def grant_currency(self, grant_type: GrantType) -> GrantCurrency:
        """
        Determines the currency of a grant's funds, based on the type of grant

        Currently assumes:
          * 100% of UKRI standard/large grants are awarded in Pounds Sterling
          * 100% of EU standard grants are awarded in Euros
          * 80% of Other grants are awarded in Pounds Sterling
          * 10% of Other grants are awarded in Euros
          * 10% of Other grants are awarded in US Dollars

        :type grant_type: GrantType
        :param grant_type: member of the GrantType enumerated class

        :example: GrantCurrency.GBP
        :rtype: GrantCurrency
        :return: member of the GrantCurrency enumerated class, representing the currency of the funds for a grant
        """
        if grant_type == GrantType.UKRI_LARGE_GRANT or grant_type == GrantType.UKRI_STANDARD_GRANT:
            return GrantCurrency.GBP
        if grant_type == GrantType.EU_STANDARD_GRANT:
            return GrantCurrency.EUR

        return GrantCurrency(self.random_element({
            GrantCurrency.GBP: 0.80,
            GrantCurrency.EUR: 0.10,
            GrantCurrency.USD: 0.10
        }))

    def grant_reference(self, grant_type: GrantType) -> str:
        """
        Generates a fake grant reference, based on the type of grant

        Currently assumes all grant references are a 20 character random string

        :type grant_type: GrantType
        :param grant_type: member of the GrantType enumerated class

        :example: 'ZmCRCKzQymLfZdNyXoJp'
        :rtype: str
        :return: fake grant reference
        """
        lengths = {
            'UKRI_STANDARD_GRANT': 20,
            'UKRI_LARGE_GRANT': 20,
            'EU_STANDARD_GRANT': 20,
            'OTHER': 20
        }
        return self.faker.pystr(max_chars=lengths[grant_type.name])

    def total_funds(self, grant_type: GrantType) -> int:
        """
        Generates a fake value for the total amount of money awarded through a grant, based on the type of grant

        Currently assumes:
          * UKRI standard grants are awarded between 1,000 and 50,000
          * UKRI large grants are awarded between 50,000 and 1,000,000
          * EU standard grants are awarded between 25,000 and 2,000,000
          * Other grants are awarded between 100 and 25,000

        :type grant_type: GrantType
        :param grant_type: member of the GrantType enumerated class

        :example: 12,345
        :rtype: int
        :return: total amount of money awarded through a grant
        """
        grants_ranges = {
            'UKRI_STANDARD_GRANT': (1000, 50000),
            'UKRI_LARGE_GRANT': (50000, 1000000),
            'EU_STANDARD_GRANT': (25000, 2000000),
            'OTHER': (100, 25000)
        }
        return self.generator.random_int(
            min=grants_ranges[grant_type.name][0],
            max=grants_ranges[grant_type.name][1]
        )

    @staticmethod
    def status(grant_duration: DateRange) -> GrantStatus:
        """
        Determines the status of a grant based on its duration

        :type grant_duration: DateRange
        :param grant_duration: duration of a project

        :example: GrantStatus.Active
        :rtype: GrantStatus
        :return: member of the GrantStatus enumerated class indicating the status of a project
        """
        if grant_duration.upper_inf:
            return GrantStatus.Active

        if grant_duration.upper > date.today():
            return GrantStatus.Active

        return GrantStatus.Closed
