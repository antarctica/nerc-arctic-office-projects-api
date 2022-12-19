import re

from pathlib import Path
from typing import Dict

import simplejson as json

from jsonschema import validate
# noinspection PyPackageRequirements
from sqlalchemy import exists
from sqlalchemy_utils import Ltree

from arctic_office_projects_api.extensions import db
from arctic_office_projects_api.utils import generate_neutral_id
from arctic_office_projects_api.models import CategoryScheme, CategoryTerm, Organisation


def import_category_terms_from_file_interactively(categories_file_path: str):
    """
    Command to import category terms and schemes from an import file.

    Import files are JSON encoded and must be structured according to the 'resources/categories-scheme.json' JSON
    Schema. Files will be validated against this schema prior to import. See the project README for more information.

    All errors will trigger an exception to be raised with any pending database models to be removed/flushed.

    :type categories_file_path: str
    :param categories_file_path: path to categories import file
    """
    print(f"Importing research categories from [{categories_file_path}]:")

    try:
        with open(categories_file_path, 'r') as categories_file, \
                open(Path('resources/categories-schema.json'), 'r') as categories_schema_file:
            categories_schema = json.load(categories_schema_file)
            categories_data = json.load(categories_file)
            validate(instance=categories_data, schema=categories_schema)
            print("* categories data valid and ready for import")
            print(f"* discovered {len(categories_data['schemes'])} schemes and {len(categories_data['terms'])} terms")

            print("* importing category schemes ...")
            total_schemes = len(categories_data['schemes'])
            imported_schemes = 0
            skipped_schemes = 0

            for scheme in categories_data['schemes']:
                if db.session.query(exists().where(CategoryScheme.namespace == scheme['namespace'])).scalar():
                    skipped_schemes += 1
                    continue

                category_scheme_resource = CategoryScheme(
                    neutral_id=generate_neutral_id(),
                    namespace=scheme['namespace'],
                    name=scheme['title'],
                    root_concepts=scheme['root-concepts']
                )
                if 'acronym' in scheme and scheme['acronym'] is not None:
                    category_scheme_resource.acronym = scheme['acronym']
                if 'description' in scheme and scheme['description'] is not None:
                    category_scheme_resource.description = scheme['description']
                if 'version' in scheme and scheme['version'] is not None:
                    category_scheme_resource.version = scheme['version']
                if 'revision' in scheme and scheme['revision'] is not None:
                    category_scheme_resource.revision = scheme['revision']
                db.session.add(category_scheme_resource)
                imported_schemes += 1

            print(f"* ... finished importing category schemes [{imported_schemes} imported, "
                  f"{skipped_schemes} already exist, {total_schemes} total]")

            print("* importing category terms, this may take some time...")
            total_categories = len(categories_data['terms'])
            imported_categories = 0
            skipped_categories = 0

            for term in categories_data['terms']:
                if db.session.query(exists().where(CategoryTerm.scheme_identifier == term['subject'])).scalar():
                    skipped_categories += 1
                    continue

                category_term_resource = CategoryTerm(
                    neutral_id=generate_neutral_id(),
                    scheme_identifier=term['subject'],
                    name=term['pref-label'],
                    path=_generate_category_term_ltree_path(term['path']),
                    category_scheme=CategoryScheme.query.filter_by(
                        namespace=term['scheme']
                    ).one()
                )
                if 'notation' in term and term['notation'] is not None:
                    category_term_resource.scheme_notation = term['notation']
                if 'alt-labels' in term and len(term['alt-labels']) > 0:
                    category_term_resource.aliases = term['alt-labels']
                if 'definitions' in term and len(term['definitions']) > 0:
                    category_term_resource.definitions = term['definitions']
                if 'examples' in term and len(term['examples']) > 0:
                    category_term_resource.examples = term['examples']
                if 'notes' in term and len(term['notes']) > 0:
                    category_term_resource.notes = term['notes']
                if 'scope-notes' in term and len(term['scope-notes']) > 0:
                    category_term_resource.scope_notes = term['scope-notes']

                db.session.add(category_term_resource)
                imported_categories += 1

            print(f"* ... finished importing category terms [{imported_categories} imported, "
                  f"{skipped_categories} already exist, {total_categories} total]")

            db.session.commit()
            print("Finished importing research categories")
    except Exception as e:
        db.session.rollback()
        # Remove any added, but non-committed, entities
        db.session.flush()
        raise e


def import_organisations_from_file_interactively(organisations_file_path: str):
    """
    Command to import organisations from an import file.

    Import files are JSON encoded and must be structured according to the 'resources/organisations-scheme.json' JSON
    Schema. Files will be validated against this schema prior to import. See the project README for more information.

    All errors will trigger an exception to be raised with any pending database models to be removed/flushed.

    :type organisations_file_path: str
    :param organisations_file_path: path to organisations import file
    """
    print(f"Importing organisations from [{organisations_file_path}]:")

    try:
        with open(organisations_file_path, 'r') as organisations_file, \
                open(Path('resources/organisations-schema.json'), 'r') as organisations_schema_file:
            organisations_schema = json.load(organisations_schema_file)
            organisations_data = json.load(organisations_file)
            validate(instance=organisations_data, schema=organisations_schema)
            print("* organisations data valid and ready for import")
            print(f"* discovered {len(organisations_data['organisations'])} organisations")

            print("* importing organisations ...")
            total_organisations = len(organisations_data['organisations'])
            imported_organisations = 0
            skipped_organisations = 0

            for organisation in organisations_data['organisations']:
                if db.session.query(exists().where(
                    Organisation.ror_identifier == organisation['ror-identifier']
                )).scalar():
                    skipped_organisations += 1
                    continue

                organisation_resource = Organisation(
                    neutral_id=generate_neutral_id(),
                    ror_identifier=organisation['ror-identifier'],
                    name=organisation['name']
                )
                if 'acronym' in organisation and organisation['acronym'] is not None:
                    organisation_resource.acronym = organisation['acronym']
                if 'website' in organisation and organisation['website'] is not None:
                    organisation_resource.website = organisation['website']
                if 'logo-url' in organisation and organisation['version'] is not None:
                    organisation_resource.logo_url = organisation['logo-url']
                db.session.add(organisation_resource)
                imported_organisations += 1

            print(f"* ... finished importing organisations [{imported_organisations} imported, "
                  f"{skipped_organisations} already exist, {total_organisations} total]")

            db.session.commit()
            print("Finished importing organisations")
    except Exception as e:
        db.session.rollback()
        # Remove any added, but non-committed, entities
        db.session.flush()
        raise e


def _generate_category_term_ltree_path(path_elements: Dict[str, str]) -> Ltree:
    """
    Converts a series of parent Category Terms into an ltree column compatible value

    Category Terms are hierarchical, with parent terms representing broader categories and children, narrower
    categories. Currently this hierarchy is represented as a tree data structure, implemented in the underlying
    database using an 'ltree' data type (https://www.postgresql.org/docs/current/ltree.html).

    This data type stores the path from the current item to the root item, including any intermediate/ancestor items.
    This path is represented as a `.` separated string of labels for each item.

    For example, the path from an item to the root item could be: [Item] -> [Parent Item] -> [Root Item]. When encoded
    as an ltree path this becomes: '[Root Item].[Parent Item].[Item]'. Labels are limited to alphanumeric characters
    and underscores - i.e. 'root_item.parent_item.item'.

    Categories used in this project are usually taken from RDF vocabularies, which typically use URIs to identify each
    concept/category. The category JSON Schema used to structure imported categories consistently requires the path of
    each category to be expressed as a list of identifiers, consequently these are typically lists of URIs.

    As these identifiers cannot be used in an ltree path encoding, this method converts them into 'ltree safe' versions
    by replacing any non-alphanumeric or underscore character with an underscore.

    For example, `['http://example.com/12', 'http://example.com/1']` becomes `'http_example_com_12.http_example_com_1'`.

    :type path_elements: list
    :param path_elements: category scheme identifiers for the categories between a category and the root category

    :rtype Ltree
    :return version of the categories path encoded as a ltree data type path expression
    """
    if len(path_elements.values()) == 0:
        raise ValueError("Path for category cannot be empty")

    path = list(map(lambda subject: re.sub('[^0-9a-zA-Z]+', '_', subject), path_elements.values()))
    return Ltree('.'.join(path))
