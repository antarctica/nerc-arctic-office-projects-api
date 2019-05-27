from datetime import timedelta
from typing import List

from faker import Faker
from faker.providers import BaseProvider
# noinspection PyPackageRequirements
from psycopg2.extras import DateRange

from arctic_office_projects_api.main.faker.providers.grant import GrantType

localized = False


class Provider(BaseProvider):
    faker = Faker()

    def project_type(self) -> GrantType:
        """
        Determines the 'type' of project based on it's grant type (e.g. UKRI standard grant, EU grant, etc.)

        Currently assumes:
         * 70% of projects are UKRI grants, 5% of which are large (split) grants
         * 10% of projects are EU grants
         * 20% of projects are 'other' grants (a mixture of internal University grants, government, NGOs, etc.)

        :example: GrantType.UKRI_STANDARD_GRANT
        :rtype: GrantType
        :return: member of the GrantType enumerated class, representing the type of grant a project is created from
        """
        return GrantType(self.random_element({
            'ukri-standard-grant': 0.665,
            'ukri-large-grant': 0.035,
            'eu-standard-grant': 0.1,
            'other-grant': 0.2
        }))

    def title(self) -> str:
        """
        Generates a fake project title

        Currently assumes:
         * 25% of project titles are between 4 and 119 words
         * 70% of project titles are between 120 and 149 words
         * 5% of project titles are between 150 and 200 words

        :example: 'Defense others economy cabinet elated'
        :rtype: str
        :return: fake project title
        """
        title_ranges = {
            '4-119': (4, 119),
            '120-149': (120, 149),
            '150-200': (150, 200)
        }
        title_range = self.random_element({'4-119': 0.25, '120-149': 0.7, '150-200': 0.05})
        return ' '.join(self.faker.words(self.generator.random_int(
            min=title_ranges[title_range][0],
            max=title_ranges[title_range][1]
        ))).capitalize()

    def has_acronym(self, grant_type: GrantType) -> bool:
        """
        Determines whether a project has an acronym or not, based on the type of grant a project is created from

        Currently assumes:
          * 92% of UKRI standard/large grant based projects have an acronym
          * 100% of EU standard grant based projects have an acronym
          * 50% of Other grant based projects have an acronym

        :type grant_type: GrantType
        :param grant_type: member of the GrantType enumerated class

        :example: True
        :rtype: bool
        :return: whether a project has an acronym
        """
        chances = {
            'UKRI_STANDARD_GRANT': (0.92, 0.08),
            'UKRI_LARGE_GRANT': (0.92, 0.08),
            'EU_STANDARD_GRANT': (1, 0),
            'OTHER': (0.5, 0.5)
        }
        return self.random_element({True: chances[grant_type.name][0], False: chances[grant_type.name][1]})

    def acronym(self) -> str:
        """
        Generates a fake project acronym

        :example: 'TEAR'
        :rtype: str
        :return: fake project acronym
        """
        return self.faker.word().upper()

    def abstract(self) -> str:
        """
        Generates a fake project abstract

        Abstract lengths are considered in terms of page lengths (e.g. 1/2 page, 1 page, 2 pages etc.), which are
        implemented as paragraph ranges (i.e. between n and N paragraphs), each with a probability. Each paragraph then
        has a random number of sentences.

        Currently assumes:
          * 15% of project abstracts are 1/2 a page (between 2 and 3 paragraphs)
          * 80% of project abstracts are 1 page (between 4 and 6 paragraphs)
          * 5% of project abstracts are 2 pages or more (between 7 and 12 paragraphs)

        :example: 'xxx ...'
        :rtype: str
        :return: fake project abstract
        """
        abstract = ''
        abstract_ranges = {
            '2-3': (2, 3),
            '4-6': (4, 7),
            '7-12': (8, 12)
        }
        abstract_range = self.random_element({'2-3': 0.15, '4-6': 0.8, '7-12': 0.05})
        for i in range(0, self.generator.random_int(
            min=abstract_ranges[abstract_range][0],
            max=abstract_ranges[abstract_range][1]
        )):
            abstract += self.faker.paragraph(self.generator.random_int(min=3, max=8))
        return abstract

    def has_website(self, grant_type: GrantType) -> bool:
        """
        Determines whether a project has a website or not, based on the type of grant a project is created from

        Currently assumes:
          * 15% of UKRI standard grant based projects have a website
          * 96% of UKRI large grant based projects have a website
          * 100% of EU standard grant based projects have a website
          * 75% of Other grant based projects have a website

        :type grant_type: GrantType
        :param grant_type: member of the GrantType enumerated class

        :example: True
        :rtype: bool
        :return: whether a project has a website
        """
        chances = {
            'UKRI_STANDARD_GRANT': (0.15, 0.85),
            'UKRI_LARGE_GRANT': (0.96, 0.04),
            'EU_STANDARD_GRANT': (1, 0),
            'OTHER': (0.75, 0.25)
        }
        return self.random_element({True: chances[grant_type.name][0], False: chances[grant_type.name][1]})

    def has_publications(self) -> bool:
        """
        Determines whether a project has any publications or not

        Currently assumes 99% of projects will have some.

        :example: True
        :rtype: bool
        :return: whether a project has any publications
        """
        return self.random_element({True: 0.99, False: 0.01})

    def publication(self) -> str:
        """
        Generates a fake DOI

        Generated DOIs are based on the CrossRef 'fake DOI' [1] 'https://doi.org/10.5555/12345678'.

        [1] https://www.crossref.org/blog/doi-like-strings-and-fake-dois/

        :example: 'https://doi.org/10.5555/12345678'
        :rtype: str
        :return: a fake, random, DOI
        """
        return f"https://doi.org/10.5555/{ str(self.generator.random_int(min=0, max=99999999)).zfill(8) }"

    def publications_list(self) -> List[str]:
        """
        Generates a list of fake DOIs

        Currently assumes:
         * 20% of projects have between 1 and 4 publications
         * 72% of projects have between 5 and 8 publications
         * 5% of projects have between 9 and 16 publications
         * 3% of projects have between 17 and 30 publications

        :example: ['https://doi.org/10.5555/12345678', 'https://doi.org/10.5555/23456789']
        :rtype: list
        :return: a list of fake DOIs
        """
        publications_ranges = {
            '1-4': (1, 4),
            '5-8': (5, 8),
            '9-16': (9, 16),
            '17-30': (17, 30)
        }
        publications_range = self.random_element({'1-4': 0.2, '5-8': 0.72, '9-16': 0.05, '17-30': 0.03})

        publications = []
        for i in range(1, self.generator.random_int(
            min=publications_ranges[publications_range][0],
            max=publications_ranges[publications_range][1]
        )):
            publications.append(self.publication())

        return publications

    def project_duration(self, grant_type: GrantType) -> DateRange:
        """
        Generates a fake project duration, based on the type of grant a project is created from

        Currently assumes:
          * all projects start within a 6 year period, starting 5 years ago (meaning some projects will start this year)
          * UKRI standard grant based projects have a duration of 3 years
          * UKRI large grant based projects have a duration of 4 years
          * EU standard grant based projects have a duration of 5 years
          * Other grant based projects have a duration of 1 year

        :type grant_type: GrantType
        :param grant_type: member of the GrantType enumerated class

        :example: DateRange(2012-01-01, 2016-01-31)
        :rtype: DateRange
        :return: the duration of a project
        """
        durations = {
            'UKRI_STANDARD_GRANT': 365 * 3,
            'UKRI_LARGE_GRANT': 365 * 4,
            'EU_STANDARD_GRANT': 365 * 5,
            'OTHER': 365 * 1
        }

        start_date = self.faker.past_date(start_date='-5y')
        if self.random_element({True: 0.1666, False: 0.8334}):
            start_date = self.faker.date_this_year(before_today=True, after_today=True)

        end_date = start_date + timedelta(days=durations[grant_type.name])

        return DateRange(start_date, end_date)

    def has_existing_principle_investigator(self) -> bool:
        """
        Determines whether a project's Principle Investigator has lead other projects and should not result a new PI

        Currently assumes 70% of projects will be lead by an existing PI

        :example: True
        :rtype: bool
        :return: whether a project has an existing Principle Investigator
        """
        return self.random_element({True: 0.7, False: 0.3})

    def has_existing_principle_investigator_organisation(self) -> bool:
        """
        Determines whether a project with a new Principle Investigator is from an existing organisation and should
        result in a new organisation for the PI

        Currently assumes 75% of PIs will be from an existing organisation

        :example: True
        :rtype: bool
        :return: whether a project with a new Principle Investigator is from an existing organisation
        """
        return self.random_element({True: 0.75, False: 0.25})

    def has_co_investigators(self) -> bool:
        """
        Determines whether a project has any Co-Investigators or not

        Currently assumes 50% of projects will have some.

        :example: True
        :rtype: bool
        :return: whether a project has any Co-Investigators
        """
        return self.random_element({True: 0.5, False: 0.5})

    def co_investigator_count(self) -> int:
        """
        Generates the number of Co-Investigators in a project

        Currently assumes:
         * 85% of projects have between 1 and 3 Co-Investigators
         * 10% of projects have between 4 and 6 Co-Investigators
         * 5% of projects have between 7 and 25 Co-Investigators

        :example: 2
        :rtype: int
        :return: the number of Co-Investigators in a project
        """
        co_investigator_ranges = {
            '1-3': (1, 3),
            '4-6': (4, 6),
            '7-25': (7, 25)
        }
        co_investigator_range = self.random_element({'1-3': 0.85, '4-6': 0.1, '7-25': 0.05})
        return self.generator.random_int(
            min=co_investigator_ranges[co_investigator_range][0],
            max=co_investigator_ranges[co_investigator_range][1]
        )

    def has_existing_co_investigator(self) -> bool:
        """
        Determines whether a project's Co-Investigator has been in other projects and should not result a new Co-I

        Currently assumes 70% of Co-Investigators will have been in other projects

        :example: True
        :rtype: bool
        :return: whether a project has an existing Co-Investigator
        """
        return self.random_element({True: 0.7, False: 0.3})

    def has_existing_co_investigator_organisation(self) -> bool:
        """
        Determines whether a project with a new Co-Investigator is from an existing organisation and should
        result in a new organisation for the Co-I

        Currently assumes 80% of Co-Is will be from an existing organisation

        :example: True
        :rtype: bool
        :return: whether a project with a new Co-Investigator is from an existing organisation
        """
        return self.random_element({True: 0.8, False: 0.2})
