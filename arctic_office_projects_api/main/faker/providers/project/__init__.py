from typing import List

from faker import Faker
from faker.providers import BaseProvider
# noinspection PyPackageRequirements
from psycopg2.extras import DateRange

localized = False


class Provider(BaseProvider):
    faker = Faker()

    def has_acronym(self) -> bool:
        """
        Determines whether a project has an acronym or not

        Currently assumes 30% of projects will have one.

        :example: True
        :rtype: bool
        :return: whether a project has an acronym
        """
        return self.random_element({True: 0.3, False: 0.6})

    def abstract(self) -> str:
        """
        Generates a fake project abstract

        :example: 'xxx ...'
        :rtype: str
        :return: Fake project abstract
        """
        return self.faker.text(self.generator.random_int(min=2500, max=7500))

    def has_website(self) -> bool:
        """
        Determines whether a project has a website or not

        Currently assumes 15% of projects will have one.

        :example: True
        :rtype: bool
        :return: whether a project has an website
        """
        return self.random_element({True: 0.15, False: 0.85})

    def has_publications(self) -> bool:
        """
        Determines whether a project has any publications or not

        Currently assumes 80% of projects will have some.

        :example: True
        :rtype: bool
        :return: whether a project has any publications
        """
        return self.random_element({True: 0.8, False: 0.2})

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

        :example: ['https://doi.org/10.5555/12345678', 'https://doi.org/10.5555/23456789']
        :rtype: list
        :return: a list of fake DOIs
        """
        publications = []
        for i in range(3):
            publications.append(self.publication())

        return publications

    def has_impact_statements(self) -> bool:
        """
        Determines whether a project has any impact statements or not

        Currently assumes 10% of projects will have some.

        :example: True
        :rtype: bool
        :return: whether a project has any impact statements
        """
        return self.random_element({True: 0.1, False: 0.9})

    def impact_statement(self) -> str:
        """
        Generates a fake impact statement

        :example: 'xxx ...'
        :rtype: str
        :return: a fake impact statement
        """
        return self.faker.paragraph(3)

    def impact_statements(self) -> List[str]:
        """
        Generates a list of fake impact statements

        :example: ['xxx ...', 'xxx ...']
        :rtype: list
        :return: a list of fake impact statements
        """
        impact_statements = []
        for i in range(3):
            impact_statements.append(self.impact_statement())

        return impact_statements

    def has_notes(self) -> bool:
        """
        Determines whether a project has any notes or not

        Currently assumes 10% of projects will have some.

        :example: True
        :rtype: bool
        :return: whether a project has any notes
        """
        return self.random_element({True: 0.1, False: 0.9})

    def note(self) -> str:
        """
        Generates a fake note

        :example: 'xxx ...'
        :rtype: str
        :return: a fake note
        """
        return self.faker.paragraph(3)

    def notes(self) -> List[str]:
        """
        Generates a list of fake notes

        :example: ['xxx ...', 'xxx ...']
        :rtype: list
        :return: a list of fake notes
        """
        notes = []
        for i in range(3):
            notes.append(self.note())

        return notes

    def project_duration(self) -> DateRange:
        """
        Generates a fake project duration

        The project duration represents the period during which the project was active.

        :rtype: DateRange
        :return: the duration of a project
        """
        start_date = self.faker.past_date(start_date='-10y')
        return DateRange(start_date, start_date.replace(start_date.year + 3))
