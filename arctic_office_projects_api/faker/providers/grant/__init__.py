import math

from datetime import date
from enum import Enum
from typing import Optional

from collections import OrderedDict

from faker import Faker
from faker.providers import BaseProvider

# noinspection PyPackageRequirements
from psycopg2.extras import DateRange
from urllib.parse import quote_plus

localized = False


class UKRICouncil(Enum):
    """
    Represents the research councils within UK Research and Innovation (UKRI)
    """

    AHRC = {"acronym": "AHRC", "prefix": "AH"}
    BBSRC = {"acronym": "BBSRC", "prefix": "BB"}
    EPSRC = {"acronym": "EPSRC", "prefix": "EP"}
    ESRC = {"acronym": "ESRC", "prefix": "ES"}
    MRC = {"acronym": "MRC", "prefix": "G"}
    NERC = {"acronym": "NERC", "prefix": "NE"}
    STFC = {"acronym": "STFC", "prefix": "ST"}


class GrantCurrency(Enum):
    """
    Represents the various currencies of a research grant
    """

    GBP = {"iso_4217_code": "GBP", "major_symbol": "£"}
    EUR = {"iso_4217_code": "EUR", "major_symbol": "€"}
    NOK = {"iso_4217_code": "NOK", "major_symbol": "kr"}
    CAD = {"iso_4217_code": "CAD", "major_symbol": "$"}


class GrantType(Enum):
    UKRI_STANDARD_GRANT = "ukri-standard-grant"
    UKRI_LARGE_GRANT = "ukri-large-grant"
    EU_STANDARD_GRANT = "eu-standard-grant"
    OTHER = "other-grant"


class GrantStatus(Enum):
    """
    Represents the various states of a research grant
    """

    Accepted = {"title": "accepted"}
    Active = {"title": "active"}
    Approved = {"title": "approved"}
    Authorised = {"title": "active"}
    Closed = {"title": "closed"}
    Completed = {"title": "completed"}
    Terminated = {"title": "terminated"}
    Pending = {"title": "pending"}

class Provider(BaseProvider):
    faker = Faker()

    def grant_currency(self, grant_type: GrantType) -> GrantCurrency:
        """
        Determines the currency of a grant's funds, based on the type of grant

        Currently assumes:
          * 100% of UKRI standard/large grants are awarded in Pounds Sterling
          * 100% of EU standard grants are awarded in Euros
          * 87.5% of Other grants are awarded in Pounds Sterling
          * 10% of Other grants are awarded in Euros
          * 2% of Other grants are awarded in Norwegian Krone
          * 0.5% of Other grants are awarded in Canadian Dollars

        :type grant_type: GrantType
        :param grant_type: member of the GrantType enumerated class

        :example: GrantCurrency.GBP
        :rtype: GrantCurrency
        :return: member of the GrantCurrency enumerated class, representing the currency of the funds for a grant
        """
        if (
            grant_type is GrantType.UKRI_LARGE_GRANT
            or grant_type is GrantType.UKRI_STANDARD_GRANT
        ):
            return GrantCurrency.GBP
        if grant_type is GrantType.EU_STANDARD_GRANT:
            return GrantCurrency.EUR

        # Use OrderedDict for weighted elements
        currency_weights = OrderedDict(
            {
                GrantCurrency.GBP: 0.875,
                GrantCurrency.EUR: 0.10,
                GrantCurrency.NOK: 0.02,
                GrantCurrency.CAD: 0.005,
            }
        )

        return GrantCurrency(self.random_element(currency_weights))

    def grant_reference(
        self, grant_type: GrantType, ukri_council: Optional[UKRICouncil]
    ) -> str:
        """
        Generates a fake grant reference, based on the type of grant and optionally UKRI council

        :type grant_type: GrantType
        :param grant_type: member of the GrantType enumerated class
        :type grant_type: UKRICouncils
        :param grant_type: member of the UKRI councils enumerated class, if a UKRI GrantType

        :example: 'NE/A00123/1' (UKRI), '000123' (EU), 'ZmCRCKzQymLfZdNyXoJp' (Other)
        :rtype: str
        :return: fake grant reference
        """
        if (grant_type is GrantType.UKRI_LARGE_GRANT and ukri_council is not None) or (
            grant_type is GrantType.UKRI_STANDARD_GRANT and ukri_council is not None
        ):
            version = self.random_element(
                OrderedDict([(1, 0.98), (2, 0.016), (3, 0.004)])
            )
            return (
                f"{ UKRICouncil(ukri_council).value['prefix'] }/{ self.faker.random_uppercase_letter() }"
                f"{ str(self.generator.random_int(min=1, max=999999)).zfill(5) }/{ version }"
            )
        elif grant_type is GrantType.EU_STANDARD_GRANT:
            return str(self.generator.random_int(min=1, max=999999)).zfill(6)

        return self.faker.pystr(max_chars=20)

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
            "UKRI_STANDARD_GRANT": (1000, 80000),
            "UKRI_LARGE_GRANT": (3000000, 3700000),
            "EU_STANDARD_GRANT": (2000000, 10000000),
            "OTHER": (100, 300000),
        }
        total_funds = self.generator.random_int(
            min=grants_ranges[grant_type.name][0], max=grants_ranges[grant_type.name][1]
        )
        # Round to nearest 100
        return int(math.floor(total_funds / 100.0)) * 100

    @staticmethod
    def grant_status(grant_duration: DateRange) -> GrantStatus:
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

    def grant_funder(self, grant_type: GrantType) -> Optional[str]:
        if (
            grant_type is GrantType.UKRI_LARGE_GRANT
            or grant_type is GrantType.UKRI_STANDARD_GRANT
        ):
            return UKRICouncil(
                self.random_element(
                    OrderedDict(
                        [
                            (UKRICouncil.AHRC, 3.4),
                            (UKRICouncil.BBSRC, 1.9),
                            (UKRICouncil.EPSRC, 1.7),
                            (UKRICouncil.ESRC, 1.7),
                            (UKRICouncil.MRC, 0),
                            (UKRICouncil.NERC, 91),
                            (UKRICouncil.STFC, 0.3),
                        ]
                    )
                )
            ).name
        elif grant_type is GrantType.EU_STANDARD_GRANT:
            return "EU"
        elif grant_type is GrantType.OTHER:
            return self.random_element(OrderedDict([(True, 0.8), (None, 0.2)]))

        return None  # pragma: no cover

    def grant_website(self, grant_type: GrantType, grant_reference: str) -> str:
        """
        Generates a fake grant website, based on the type of grant

        :type grant_type: GrantType
        :param grant_type: member of the GrantType enumerated class

        :type grant_reference: str
        :param grant_reference: fake grant reference

        :example: 'https://gtr.ukri.org/projects?ref=ST%2FF006446%2F1' (UKRI),
        'https://cordis.europa.eu/project/rcn/217700' (EU), 'https://www.example.com/123abc' (Other)
        :rtype: str
        :return: fake grant website
        """
        if (
            grant_type is GrantType.UKRI_LARGE_GRANT
            or grant_type is GrantType.UKRI_STANDARD_GRANT
        ):
            return f"https://gtr.ukri.org/projects?ref={ quote_plus(grant_reference) }"
        elif grant_type is GrantType.EU_STANDARD_GRANT:
            return (
                f"https://cordis.europa.eu/project/rcn/{ quote_plus(grant_reference) }"
            )

        return self.faker.uri()  # pragma: no cover
