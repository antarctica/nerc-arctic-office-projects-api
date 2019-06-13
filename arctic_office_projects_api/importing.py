import re

from datetime import date
from pathlib import Path
from typing import Dict
from urllib.parse import quote as url_encode

import requests
import simplejson as json

from jsonschema import validate
from psycopg2.extras import DateRange
from requests import HTTPError
# noinspection PyPackageRequirements
from sqlalchemy import exists
from sqlalchemy_utils import Ltree

from arctic_office_projects_api.extensions import db
from arctic_office_projects_api.utils import generate_neutral_id
from arctic_office_projects_api.models import CategoryScheme, CategoryTerm, Grant, GrantStatus, GrantCurrency, \
    Organisation, Project, Allocation, Person, Participant, ParticipantRole, Categorisation


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


def import_gateway_to_research_grant_interactively(grant_reference: str):
    print(f"Importing Gateway to Research (GTR) project with grant reference ({grant_reference})")

    if db.session.query(exists().where(
        Organisation.grid_identifier == 'https://www.grid.ac/institutes/grid.8682.4'
    )).scalar():
        print(f"* ... finished importing Gateway to Research project with grant reference ({grant_reference}), already exists")

    print(f"Searching GTR for project with grant reference ({grant_reference})")
    try:
        gtr_project_response = requests.get(
            url=f"https://gtr.ukri.org/gtr/api/projects",
            params={
                'q': url_encode(grant_reference),
                'f': 'pro.gr'
            },
            headers={
                'accept': 'application/vnd.rcuk.gtr.json-v7'
            }
        )
        gtr_project_response.raise_for_status()
        gtr_project_data = gtr_project_response.json()
        if 'project' not in gtr_project_data:
            raise KeyError("Project element not in GTR response")
        if len(gtr_project_data['project']) != 1:
            raise ValueError("Multiple project elements found in GTR response, only expected one")
        gtr_project = gtr_project_data['project'][0]
        print(f"Found GTR project for grant reference ({grant_reference}) - [{gtr_project['id']}]")

        grant = Grant(neutral_id=generate_neutral_id())
        if 'identifiers' not in gtr_project:
            raise KeyError("Identifiers element not in GTR project")
        if 'identifier' not in gtr_project['identifiers']:
            raise KeyError("Identifiers list element not in GTR project")
        grant.reference = None
        for gtr_identifier in gtr_project['identifiers']['identifier']:
            if 'value' in gtr_identifier and gtr_identifier['value'] == grant_reference:
                grant.reference = gtr_identifier['value']
        if grant.reference is None:
            raise KeyError("Grant identifier not found in GTR project identifiers")
        if 'title' not in gtr_project:
            raise KeyError("Title element not in GTR project")
        grant.title = gtr_project['title']
        if 'status' not in gtr_project:
            raise KeyError("Status element not in GTR project")
        if gtr_project['status'] == 'Closed':
            grant.status = GrantStatus.Closed

        if 'abstractText' in gtr_project:
            grant.abstract = gtr_project['abstractText']

        if 'links' not in gtr_project:
            raise KeyError("Links element not in GTR project")
        if 'link' not in gtr_project['links']:
            raise KeyError("Links list element not in GTR project")

        # Silently looping
        gtr_fund_uri = None
        for gtr_project_link in gtr_project['links']['link']:
            if gtr_project_link['rel'] == 'FUND':
                gtr_fund_uri = gtr_project_link['href']
        if gtr_fund_uri is None:
            raise KeyError("Grant fund relation not found in GTR project links")
        print(f"Getting related GTR fund [{gtr_fund_uri}]")
        gtr_funds_response = requests.get(
            url=gtr_fund_uri,
            headers={
                'accept': 'application/vnd.rcuk.gtr.json-v7'
            }
        )
        gtr_funds_response.raise_for_status()
        gtr_fund = gtr_funds_response.json()
        if 'start' not in gtr_fund:
            raise KeyError('Start date element not in GTR fund')
        if 'end' not in gtr_fund:
            raise KeyError('End date element not in GTR fund')

        grant.duration = DateRange(date(2012, 1, 1), date(2015, 1, 1))

        if 'valuePounds' in gtr_fund:
            if 'currencyCode' in gtr_fund and gtr_fund['currencyCode'] == 'GBP':
                grant.total_funds_currency = GrantCurrency.GBP
            if 'amount' in gtr_fund:
                grant.total_funds = gtr_fund['amount']

        gtr_project_publications = []
        for gtr_project_link in gtr_project['links']['link']:
            if gtr_project_link['rel'] == 'PUBLICATION':
                gtr_publication_response = requests.get(
                    url=gtr_project_link['href'],
                    headers={
                        'accept': 'application/vnd.rcuk.gtr.json-v7'
                    }
                )
                gtr_publication_response.raise_for_status()
                gtr_publication = gtr_publication_response.json()
                if 'doi' in gtr_publication:
                    gtr_project_publications.append(gtr_publication['doi'])
        if len(gtr_project_publications) > 0:
            grant.publications = gtr_project_publications

        if 'links' not in gtr_fund:
            raise KeyError("Links element not in GTR fund")
        if 'link' not in gtr_fund['links']:
            raise KeyError("Links list element not in GTR fund")
        gtr_funder_uri = None
        for gtr_fund_link in gtr_fund['links']['link']:
            if gtr_fund_link['rel'] == 'FUNDER':
                gtr_funder_uri = gtr_fund_link['href']
        if gtr_funder_uri is None:
            raise KeyError("Grant funder relation not found in GTR fund links")
        if gtr_funder_uri == 'https://gtr.ukri.org:443/gtr/api/organisations/8A03ED41-E67D-4F4A-B5DD-AAFB272B6471':
            if not db.session.query(exists().where(
                Organisation.grid_identifier == 'https://www.grid.ac/institutes/grid.8682.4'
            )).scalar():
                db.session.add(Organisation(
                    neutral_id=generate_neutral_id(),
                    grid_identifier='https://www.grid.ac/institutes/grid.8682.4',
                    name='Natural Environment Research Council',
                    acronym='NERC',
                    website='https://nerc.ukri.org',
                    logo_url='https://placeimg.com/256/256/arch'
                ))
            grant.funder = Organisation.query.filter_by(grid_identifier='https://www.grid.ac/institutes/grid.8682.4').one()

        db.session.add(grant)

        project = Project(
            neutral_id=generate_neutral_id(),
            title=grant.title,
            abstract=grant.abstract,
            project_duration=grant.duration,
            access_duration=DateRange(grant.duration.lower, None),
            publications=grant.publications
        )
        db.session.add(project)

        gtr_project_categories = []
        project_categories = []
        if 'researchSubjects' in gtr_project:
            if 'researchSubject' in gtr_project['researchSubjects']:
                if len(gtr_project['researchSubjects']['researchSubject']) > 0:
                    for gtr_research_subject in gtr_project['researchSubjects']['researchSubject']:
                        gtr_project_categories.append(gtr_research_subject)
        if 'researchTopics' in gtr_project:
            if 'researchTopic' in gtr_project['researchTopics']:
                if len(gtr_project['researchTopics']['researchTopic']) > 0:
                    for gtr_research_topic in gtr_project['researchTopics']['researchTopic']:
                        gtr_project_categories.append(gtr_research_topic)
        if len(gtr_project_categories) > 0:
            for gtr_project_category in gtr_project_categories:
                if 'id' in gtr_project_category:
                    if gtr_project_category['id'] == 'E4C03353-6311-43F9-9204-CFC2536D2017':
                        project_categories.append('https://gcmdservices.gsfc.nasa.gov/kms/concept/c47f6052-634e-40ef-a5ac-13f69f6f4c2a')
                    elif gtr_project_category['id'] == 'C62D281D-F1B9-423D-BDAB-361EC9BE7C68':
                        project_categories.append('https://gcmdservices.gsfc.nasa.gov/kms/concept/286d2ae0-9d86-4ef0-a2b4-014843a98532')
                    elif gtr_project_category['id'] == 'C29F371D-A988-48F8-BFF5-1657DAB1176F':
                        pass
                    elif gtr_project_category['id'] == 'B01D3878-E7BD-4830-9503-2F54544E809E':
                        pass
        if len(project_categories) > 0:
            for project_category in project_categories:
                db.session.add(Categorisation(
                    neutral_id=generate_neutral_id(),
                    project=project,
                    category_term=CategoryTerm.query.filter_by(scheme_identifier=project_category).one()
                ))

        db.session.add(Allocation(
            neutral_id=generate_neutral_id(),
            project=project,
            grant=grant
        ))

        for gtr_project_link in gtr_project['links']['link']:
            if gtr_project_link['rel'] == 'PI_PER':
                gtr_project_pi_response = requests.get(
                    url=gtr_project_link['href'],
                    headers={
                        'accept': 'application/vnd.rcuk.gtr.json-v7'
                    }
                )
                gtr_project_pi_response.raise_for_status()
                gtr_project_pi = gtr_project_pi_response.json()

                pi = Person(
                    neutral_id=generate_neutral_id()
                )
                if 'firstName' in gtr_project_pi:
                    pi.first_name = gtr_project_pi['firstName']
                if 'surname' in gtr_project_pi:
                    pi.last_name = gtr_project_pi['surname']
                if 'orcidId' in gtr_project_pi:
                    pi.orcid_id = f"https://orcid.org/{gtr_project_pi['orcidId']}"

                gtr_project_pi_organisation_uri = None
                if 'links' not in gtr_project_pi:
                    raise KeyError("Links element not in GTR PI")
                if 'link' not in gtr_project_pi['links']:
                    raise KeyError("Links list element not in GTR PI")
                for gtr_project_pi_link in gtr_project_pi['links']['link']:
                    if gtr_project_pi_link['rel'] == 'EMPLOYED':
                        gtr_project_pi_organisation_uri = gtr_project_pi_link['href']
                if gtr_project_pi_organisation_uri is None:
                    raise KeyError("Grant employer relation not found in GTR PI links")
                gtr_project_pi_organisation_response = requests.get(
                    url=gtr_project_pi_organisation_uri,
                    headers={
                        'accept': 'application/vnd.rcuk.gtr.json-v7'
                    }
                )
                gtr_project_pi_organisation_response.raise_for_status()
                gtr_project_pi_organisation = gtr_project_pi_organisation_response.json()
                if 'name' not in gtr_project_pi_organisation:
                    raise KeyError("Name element not in GTR PI Organisation")
                if not db.session.query(exists().where(
                    Organisation.name == gtr_project_pi_organisation['name']
                )).scalar():
                    db.session.add(Organisation(
                        neutral_id=generate_neutral_id(),
                        name=gtr_project_pi_organisation['name']
                    ))
                pi.organisation = Organisation.query.filter_by(name=gtr_project_pi_organisation['name']).one()

                db.session.add(pi)

                db.session.add(Participant(
                    neutral_id=generate_neutral_id(),
                    project=project,
                    person=pi,
                    role=ParticipantRole.InvestigationRole_PrincipleInvestigator
                ))

            if gtr_project_link['rel'] == 'COI_PER':
                gtr_project_coi_response = requests.get(
                    url=gtr_project_link['href'],
                    headers={
                        'accept': 'application/vnd.rcuk.gtr.json-v7'
                    }
                )
                gtr_project_coi_response.raise_for_status()
                gtr_project_coi = gtr_project_coi_response.json()

                coi = Person(
                    neutral_id=generate_neutral_id()
                )
                if 'firstName' in gtr_project_coi:
                    coi.first_name = gtr_project_coi['firstName']
                if 'surname' in gtr_project_coi:
                    coi.last_name = gtr_project_coi['surname']
                if 'orcidId' in gtr_project_coi:
                    coi.orcid_id = f"https://orcid.org/{gtr_project_coi['orcidId']}"

                gtr_project_coi_organisation_uri = None
                if 'links' not in gtr_project_coi:
                    raise KeyError("Links element not in GTR CoI")
                if 'link' not in gtr_project_coi['links']:
                    raise KeyError("Links list element not in GTR CoI")
                for gtr_project_coi_link in gtr_project_coi['links']['link']:
                    if gtr_project_coi_link['rel'] == 'EMPLOYED':
                        gtr_project_coi_organisation_uri = gtr_project_coi_link['href']
                if gtr_project_coi_organisation_uri is None:
                    raise KeyError("Grant employer relation not found in GTR CoI links")
                gtr_project_coi_organisation_response = requests.get(
                    url=gtr_project_coi_organisation_uri,
                    headers={
                        'accept': 'application/vnd.rcuk.gtr.json-v7'
                    }
                )
                gtr_project_coi_organisation_response.raise_for_status()
                gtr_project_coi_organisation = gtr_project_coi_organisation_response.json()
                if 'name' not in gtr_project_coi_organisation:
                    raise KeyError("Name element not in GTR CoI Organisation")
                if not db.session.query(exists().where(
                    Organisation.name == gtr_project_coi_organisation['name']
                )).scalar():
                    db.session.add(Organisation(
                        neutral_id=generate_neutral_id(),
                        name=gtr_project_coi_organisation['name']
                    ))
                coi.organisation = Organisation.query.filter_by(name=gtr_project_coi_organisation['name']).one()

                db.session.add(coi)

                db.session.add(Participant(
                    neutral_id=generate_neutral_id(),
                    project=project,
                    person=coi,
                    role=ParticipantRole.InvestigationRole_CoInvestigator
                ))

        db.session.commit()
        print(f"* ... finished importing Gateway to Research project [{gtr_project['id']}], for grant reference "
              f"({grant_reference})")
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
