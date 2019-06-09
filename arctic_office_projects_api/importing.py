import re
from pathlib import Path
from typing import Dict

import simplejson as json
from jsonschema import validate
# noinspection PyPackageRequirements
from sqlalchemy import exists
from sqlalchemy_utils import Ltree

from arctic_office_projects_api import db
from arctic_office_projects_api.utils import generate_neutral_id
from arctic_office_projects_api.models import CategoryScheme, CategoryTerm


def import_category_terms_from_file_interactively(categories_file_path: str):
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


def _generate_category_term_ltree_path(path_elements: Dict[str, str]) -> Ltree:
    if len(path_elements.values()) == 0:
        raise ValueError("Path for category cannot be empty")

    path = list(map(lambda subject: re.sub('[^0-9a-zA-Z]+', '_', subject), path_elements.values()))
    return Ltree('.'.join(path))
