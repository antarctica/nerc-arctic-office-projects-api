from tests.base_test import BaseCommandTestCase


class InbuiltCommandsTestCase(BaseCommandTestCase):
    def test_help(self):
        result = self.runner.invoke(args=['--help'])
        self.assertIn('Show this message and exit.', result.output)


class SeedingCommandTestCase(BaseCommandTestCase):
    def test_seeding_predictable(self):
        result = self.runner.invoke(args=['seed', 'predictable'])
        self.assertIn('Seeded predictable mock resources', result.output)

    def test_seeding_random(self):
        # Prerequisites
        self.runner.invoke(args=['import', 'categories', 'tests/resources/science-categories.json'])
        self.runner.invoke(args=['import', 'organisations', 'tests/resources/funder-organisations.json'])

        result = self.runner.invoke(args=['seed', 'random'])
        self.assertIn('Seeded random mock resources', result.output)


class ImportCommandTestCase(BaseCommandTestCase):
    def test_import_categories_from_file(self):
        result = self.runner.invoke(args=['import', 'categories', 'tests/resources/science-categories.json'])
        self.assertIn('Finished importing research categories', result.output)

    def test_import_organisations_from_file(self):
        result = self.runner.invoke(args=['import', 'organisations', 'tests/resources/funder-organisations.json'])
        self.assertIn('Finished importing organisations', result.output)

    def test_import_grant_from_gtr(self):
        # Prerequisites
        self.runner.invoke(args=['import', 'categories', 'tests/resources/science-categories.json'])
        self.runner.invoke(args=['import', 'organisations', 'tests/resources/funder-organisations.json'])
        self.runner.invoke(args=['import', 'organisations', 'tests/resources/people-organisations.json'])

        result = self.runner.invoke(args=['import', 'grant', 'gtr', 'NE/K011820/1'])
        self.assertIn('Finished importing GTR project', result.output)
